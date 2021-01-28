"""Implements classes for audio playback.

Example:
    >>> from engine import resource
    >>> music = AudioSource(resource.path("music/theme.wav"), loop=True)
    >>> music.play()
    >>> import time
    >>> time.sleep(10)
    >>> music.stop()
"""
import atexit
import ctypes
import wave
# TODO(@bveeramani): I'm not sure why, but pytype tweaks about the `channels`,
# `buffer`, `length`, and `frequency` attributes of the `AudioFile` class.
# pytype: disable=attribute-error

# pylint: disable=wildcard-import, unused-wildcard-import
# pytype: disable=name-error
# TODO(@bveeramani): Remove wildcard import or fork the PyOpenAL library and
# remove members that are not prefixed with "al".
from openal import *

from engine import resource

_DEVICE = alcOpenDevice(None)
if not _DEVICE:
    raise RuntimeError("Failed to open default OpenAL device.")

_CONTEXT = alcCreateContext(_DEVICE, None)
if not _CONTEXT:
    raise RuntimeError("Failed to create OpenAL context.")

alcMakeContextCurrent(_CONTEXT)

_SOURCES = []
_BUFFERS = []


def _exit():
    """Deallocate resources on program exit."""
    for source in _SOURCES:
        alDeleteSources(1, ctypes.pointer(source.id))
    for buffer in _BUFFERS:
        alDeleteBuffers(1, ctypes.pointer(buffer.id))
    alcDestroyContext(_CONTEXT)
    alcCloseDevice(_DEVICE)


atexit.register(_exit)


class AudioFile:  # pylint: disable=too-few-public-methods
    """Encapsulates an aribtrary audio file.

    Attributes:
        channels: An integer representing the number of audio channels. A value
            of 1 represents mono and a value of 2 represents stereo.
        frequency: An integer representing the sampling frequency.
        buffer: A bytes object containing the audio.
        length: A integer representing the length of the buffer.
    """

    def __init__(self, path: str):
        """Open an audio file and initialize attributes.

        Arguments:
            path: Path to an audio file.

        Raises:
            NotImplementedError: If the audio file is not a WAVE audio file.
        """
        try:
            file = wave.open(path)
        except wave.Error as error:
            raise NotImplementedError("The file at %s is not a WAVE file." %
                                      path) from error

        self.channels = file.getnchannels()
        self.frequency = file.getframerate()

        self.buffer = b""
        change = 1
        while change:
            # TODO(@bveeramani): Replace `4096 * 8` with a constant.
            audio_frames = file.readframes(4096 * 8)
            change = len(audio_frames)
            self.buffer += audio_frames

        self.length = len(self.buffer)

        file.close()


class AudioBuffer:  # pylint: disable=too-few-public-methods
    """Encapsulates an OpenAL buffer.

    See chapter 5 of the OpenAL specification (version 1.1):

        https://www.openal.org/documentation/openal-1.1-specification.pdf

    Attributes:
        id: A pointer to an integer that represents the ID of this buffer.
    """

    def __init__(self, file: AudioFile):
        """Generate a buffer and buffer the audio data.

        Arguments:
            file: The audio file to buffer.
        """
        _BUFFERS.append(self)

        self.id = ctypes.c_uint()
        alGenBuffers(1, ctypes.pointer(self.id))

        if file.channels == 1:
            audio_format = ctypes.c_int(AL_FORMAT_MONO16)
        elif file.channels == 2:
            audio_format = ctypes.c_int(AL_FORMAT_STEREO16)
        else:
            raise NotImplementedError("Expected 1 or 2 channels but got %d." %
                                      file.channels)

        alBufferData(self.id, audio_format, file.buffer,
                     ctypes.c_int(file.length), ctypes.c_int(file.frequency))


class AudioSource:
    """Encapsulates an OpenAL source.

    See section 4.3 of the OpenAL specification (version 1.1):

        https://www.openal.org/documentation/openal-1.1-specification.pdf

    Attributes:
        id: A pointer to an integer that represents the ID of this buffer.
    """

    def __init__(self, path: str, loop: bool = False):
        """Buffer audio data and generate an audio source.

        Arguments:
            path: Path to an audio file.
            loop: If true, then loop the audio indefinitely.
        """
        _SOURCES.append(self)

        path = resource.path(path)

        audio_file = AudioFile(path)
        buffer = AudioBuffer(audio_file)

        self.id = ctypes.c_uint()
        alGenSources(1, ctypes.pointer(self.id))
        alSourcei(self.id, AL_BUFFER, ctypes.c_int(buffer.id.value))

        alSourcei(self.id, ctypes.c_int(AL_LOOPING), ctypes.c_int(loop))

        self._volume = 1

    def play(self) -> None:
        """Play this audio."""
        alSourcePlay(self.id)

    def pause(self) -> None:
        """Pause this audio."""
        alSourcePause(self.id)

    def stop(self) -> None:
        """Stop playing this audio."""
        alSourceStop(self.id)

    @property
    def volume(self) -> float:
        """Return a number in the unit interval representing the gain."""
        return self._volume

    @volume.setter
    def volume(self, value: float):
        """Set the volume of this audio source.

        Arguments:
            value: The desired volume. If value is less than 0, then the
                volume is set to 0. If value is greater than 1, then the
                volume is set to 1.
        """
        if value < 0:
            value = 0
        if value > 1:
            value = 1
        alSourcef(self.id, ctypes.c_int(AL_GAIN), ctypes.c_float(value))
        self._volume = value

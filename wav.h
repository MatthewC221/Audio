#include <inttypes.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <err.h>

// Using this for header structure http://soundfile.sapp.org/doc/WaveFormat/

typedef struct {

    unsigned char chunkID[4];
    uint32_t chunkSize;
    unsigned char format[4];
    unsigned char subchunkID[4];
    uint32_t subchunk1Size;
    uint16_t audio_format;  // PCM = 1 (linear quantization), else compression
    uint16_t channels;      // Mono = 1, Stereo = 2, etc.
    uint32_t sample_rate;   
    uint32_t byteRate;      // SampleRate * NumChannels * BitsPerSample / 8
    uint16_t blockAlign;    // NumChannels * BitsPerSample / 8
    uint16_t BPS;            // Bits per sample
    unsigned char subchunk2ID[4];
    uint32_t subchunk2Size;
    

} WavHeader;



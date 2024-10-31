// My naive rewrite of xoshiro256 from
// https://prng.di.unimi.it/xoshiro256plusplus.c

fn rotl(x: u64, k: isize) -> u64 {
    (x << k) | (x >> (64 - k))
}

pub struct Xoshiro256 {
    s: [u64; 4],
}

impl Xoshiro256 {
    pub fn new(seed: u64) -> Self {
        // I think I'm using the seed very wrongly
        Self {
            s: [
                seed & 0xFF,
                (seed >> 16) & 0xFFFF,
                (seed >> 32) & 0xFFFF,
                (seed >> 48) & 0xFFFF,
            ],
        }
    }

    pub fn next(self: &mut Self) -> u64 {
        let res = rotl(self.s[0] + self.s[3], 23) + self.s[0];
        let t = self.s[0] << 17;

        self.s[2] ^= self.s[0];
        self.s[3] ^= self.s[1];
        self.s[1] ^= self.s[2];
        self.s[0] ^= self.s[3];

        self.s[2] ^= t;
        self.s[3] = rotl(self.s[3], 45);

        res
    }

    pub fn jump(self: &mut Self) {
        let jump: [u64; 4] = [
            0x180ec6d33cfd0aba,
            0xd5a61266f0c9392c,
            0xa9582618e03fc9aa,
            0x39abdc4529b1661c,
        ];

        let mut s0 = 0;
        let mut s1 = 0;
        let mut s2 = 0;
        let mut s3 = 0;

        for i in 0..4 {
            for b in 0..64 {
                if (jump[i] & 1 << b) != 0 {
                    s0 ^= self.s[0];
                    s1 ^= self.s[1];
                    s2 ^= self.s[2];
                    s3 ^= self.s[3];
                }
                self.next();
            }
        }

        self.s[0] = s0;
        self.s[1] = s1;
        self.s[2] = s2;
        self.s[3] = s3;
    }

    pub fn long_jump(self: &mut Self) {
        let long_jump: [u64; 4] = [
            0x76e15d3efefdcbbf,
            0xc5004e441c522fb3,
            0x77710069854ee241,
            0x39109bb02acbe635,
        ];

        let mut s0 = 0;
        let mut s1 = 0;
        let mut s2 = 0;
        let mut s3 = 0;

        for i in 0..4 {
            for b in 0..64 {
                if (long_jump[i] & 1 << b) != 0 {
                    s0 ^= self.s[0];
                    s1 ^= self.s[1];
                    s2 ^= self.s[2];
                    s3 ^= self.s[3];
                }
                self.next();
            }
        }

        self.s[0] = s0;
        self.s[1] = s1;
        self.s[2] = s2;
        self.s[3] = s3;
    }
}

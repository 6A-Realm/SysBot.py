# By: https://github.com/Z1R343L
# Thank you

BLOCKPOSITION = [0, 1, 2, 3, 0, 1, 3, 2, 0, 2, 1, 3, 0, 3, 1, 2, 0, 2, 3, 1, 0, 3, 2, 1, 1, 0, 2, 3, 1, 0, 3, 2, 2, 0, 1, 3, 3, 0, 1, 2, 2, 0, 3, 1, 3, 0, 2, 1, 1, 2, 0, 3, 1, 3, 0, 2, 2, 1, 0, 3, 3, 1, 0, 2, 2, 3, 0, 1, 3, 2, 0, 1, 1, 2, 3, 0, 1, 3, 2, 0, 2, 1, 3, 0, 3, 1, 2, 0, 2, 3, 1, 0, 3, 2, 1, 0, 0, 1, 2, 3, 0, 1, 3, 2, 0, 2, 1, 3, 0, 3, 1, 2, 0, 2, 3, 1, 0, 3, 2, 1, 1, 0, 2, 3, 1, 0, 3, 2]
blockPositionInvert = [0, 1, 2, 4, 3, 5, 6, 7, 12, 18, 13, 19, 8, 10, 14, 20, 16, 22, 9, 11, 15, 21, 17, 23, 0, 1, 2, 4, 3, 5, 6, 7]

class Pokecypto:
	def __init__(self, data: bytearray) -> None:
		self.data = data

	def __crypt__(self, seed: int, start: int, end: int) -> None:
		i = start
		while i < end:
			seed = seed * 0x41C64E6D + 0x00006073
			self.data[i] ^= (seed >> 16) & 0xFF
			i += 1
			self.data[i] ^= (seed >> 24) & 0xFF
			i += 1	

	def __cryptPKM__(self, seed: int) -> None:
		self.__crypt__(seed, 8, 0x148)
		if len(self.data) == 0x158:
			self.__crypt__(seed, 0x148, 0x158)

	def __shuffle__(self, sv: int) -> None:
		idx = 4 * sv
		sdata = bytearray(self.data[:])
		for block in range(4):
			ofs = BLOCKPOSITION[idx + block]
			self.data[8 + 0x50 * block : 8 + 0x50 * (block + 1)] = sdata[8 + 0x50 * ofs : 8 + 0x50 * (ofs + 1)]

	def __setushort(self, offset: int, p: int) -> None:
		self.data[offset:offset + 2] = (p).to_bytes(2, byteorder='little')

	def __getushort(self, offset: int) -> int:
		return int.from_bytes(self.data[offset:offset + 2], byteorder='little')

	def __getuint(self, offset: int) -> int:
		return int.from_bytes(self.data[offset:offset + 4], byteorder='little')

	def __calChecksum(self) -> int:
		chk = 0
		for i in range(8, 0x148, 2):
			chk += self.__getushort(i)
			chk &= 0xFFFF
		return chk

	def is_enc(self) -> bool:
		return self.data[0x70] != 0 and self.data[0xC0] != 0

	def __refreshChecksum(self) -> None:
		self.__setushort(0x6, self.__calChecksum())

	def ec(self) -> int:
		return self.__getuint(0x0)

	def encrypt(self) -> bytearray:
		self.__refreshChecksum()
		seed = self.ec()
		sv = (seed >> 13) & 0x1F
		self.__shuffle__(blockPositionInvert[sv])
		self.__cryptPKM__(seed)
		return self.data
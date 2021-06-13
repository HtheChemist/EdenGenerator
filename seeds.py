import numpy as np


def seed2string(seedval: int):
    aAbcdefghjklmnp = "ABCDEFGHJKLMNPQRSTWXYZ01234V6789"
    seed_checksum = 0
    tmp_seedval = 0
    v10 = []
    seed_string = ""

    if seedval:
        tmp_seedval = seedval
        while True:
            v4 = np.uint8((tmp_seedval + seed_checksum)& 0xff)
            tmp_seedval >>= 5
            seed_checksum = np.uint8((v4 >> 7) + 2 * v4)
            if not tmp_seedval:
                break

    v6 = seedval ^ 0xFEF7FFD
    v10.append(np.uint32(v6 >> 27))
    v10.append(np.uint32((v6 >> 22) & 0x1F))
    v10.append(np.uint32((v6 >> 17) & 0x1F))
    v10.append(np.uint32((v6 >> 12) & 0x1F))
    v10.append(np.uint32((v6 >> 7) & 0x1F))
    v10.append(np.uint32((v6 >> 2) & 0x1F))
    v10.append(np.uint32(((seed_checksum | (v6 << 8)) >> 5) & 0x1F))
    v10.append(np.uint32(seed_checksum & 0x1F))

    for v7 in range(0, 9):
        if v7 != 4:
            offset = 0
            if v7 > 4:
                offset = -1
            seed_string += aAbcdefghjklmnp[v10[v7 + offset]]
        else:
            seed_string += " "

    return seed_string


#
# unsigned int Seeds::String2Seed(string a1)
# {
# 	string v1; // r15@1
# 	char v3; // bl@1
# 	unsigned int v4; // rcx@2
# 	unsigned int result; // rax@4
# 	__int64 v6; // rcx@6
# 	__int64 v7; // rax@9
# 	__int64 v8; // rdx@11
# 	signed int v9; // eax@13
# 	int v10; // eax@15
# 	signed __int64 v11; // rdi@15
# 	int v12; // edi@17
# 	int v13; // edx@19
# 	unsigned int v14; // edi@20
# 	unsigned int v15; // edx@20
# 	unsigned __int8 v17[8]; // [sp+8h] [bp-128h]@17
# 	char v18[256]; // [sp+10h] [bp-120h]@9
# 	__int64 v19; // [sp+110h] [bp-20h]@1
#
# 	const char aAbcdefghjklmnp[] = "ABCDEFGHJKLMNPQRSTWXYZ01234V6789";
#
# 	v1 = a1;
# 	/*
# 	v3 = *(_BYTE *)a1 & 1;
# 	if ( v3 )
# 	v4 = *(_QWORD *)(a1 + 8);
# 	else
# 	v4 = (unsigned __int64)*(_BYTE *)a1 >> 1;
# 	*/
# 	v4 = v1.length();
# 	result = 0LL;
# 	if ( v4 == 9 )
# 	{
# 		// v6 = v3 ? *(_QWORD *)(a1 + 16) : a1 + 1;
# 		if (1)
# 		{
# 			memset(v18, 255, 0x100uLL);
# 			v7 = 0LL;
# 			do
# 			{
# 				v18[aAbcdefghjklmnp[v7]] = v7;
# 				++v7;
# 			}
# 			while ( v7 != 32 );
# 			v8 = 0LL;
# 			while ( 1 )
# 			{
# 				if ( (_DWORD)v8 != 4 )
# 				{
# 					v9 = 0;
# 					if ( (unsigned int)v8 > 4 )
# 						v9 = -1;
# 					v10 = v8 + v9;
# 					//v11 = v1 + 1;
# 					//if ( v3 )
# 					//	v11 = *(_QWORD *)(v1 + 16);
# 					//v12 = (unsigned __int8)v18[*(_BYTE *)(v11 + v8)];
# 					v12 = (unsigned __int8)v18[v1[v8]];
# 					v17[v10] = v12;
# 					result = 0LL;
# 					if ( v12 == 255 )
# 						break;
# 				}
# 				if ( (unsigned int)++v8 >= 9 )
# 				{
# 					result = 0LL;
# 					v13 = 0;
# 					if ( ((v17[0] << 27) | (v17[1] << 22) | (v17[2] << 17) | (v17[3] << 12) | (v17[4] << 7) | 4 * v17[5] | ((unsigned int)v17[6] >> 3)) != 267354109 )
# 					{
# 						LOBYTE(v14) = 0;
# 						v15 = ((v17[0] << 27) | (v17[1] << 22) | (v17[2] << 17) | (v17[3] << 12) | (v17[4] << 7) | 4 * v17[5] | ((unsigned int)v17[6] >> 3)) ^ 0xFEF7FFD;
# 						do
# 						{
# 							v14 = 2 * (unsigned __int8)(v15 + v14) | ((unsigned int)(unsigned __int8)(v15 + v14) >> 7);
# 							v15 >>= 5;
# 						}
# 						while ( v15 );
# 						v13 = (unsigned __int8)v14;
# 					}
# 					if ( v13 == (v17[7] | (32 * v17[6] & 0xE0)) )
# 						result = ((v17[0] << 27) | (v17[1] << 22) | (v17[2] << 17) | (v17[3] << 12) | (v17[4] << 7) | 4 * v17[5] | ((unsigned int)v17[6] >> 3)) ^ 0xFEF7FFD;
# 					break;
# 				}
# 			}
# 		}
# 	}
# 	return result;
# }

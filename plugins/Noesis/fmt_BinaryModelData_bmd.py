#BMD (Binary Model Data)
#Author: Cra0kalo
#Contact: me@cra0kalo.com
#Site: http://cra0kalo.com
#Version: 1.0
from inc_noesis import *


def registerNoesisTypes():
	handle = noesis.register("Binary Model Data", ".bmd")
	noesis.setHandlerTypeCheck(handle, bmdCheckType)
	noesis.setHandlerLoadModel(handle, bmdLoadModel)

	return 1


def bmdCheckType(data):
 bmd = NoeBitStream(data)
	#check Magic BMDC
 if bmd.readUInt() != 0x43444D42:
  return 0
	#check Version 1
 if bmd.readInt() != 1:
  return 0
	#check filesize
 bmd.seek(0x4, NOESEEK_REL)
 if bmd.readUInt() != len(data):
  return 0
  
 return 1

class bmdFile: 
         
	def __init__(self, bs):
		self.bs = bs
		self.meta = []
		self.boneList = []
		self.matList  = [] 	
		self.triList  = []		


	def alignPosition(self, bs, alignment):
		alignment = alignment - 1
		bs.seek(((bs.tell() + alignment) & ~alignment), NOESEEK_ABS)

	def loadAll(self, bs):
		rapi.rpgSetOption(noesis.RPGOPT_TRIWINDBACKWARD, 1)
		bs.seek(0x10, NOESEEK_ABS)
		self.loadmeta(bs)
		self.loadBones(bs)
		self.loadMaterialList(bs)
		self.loadTriangleList(bs)
		#pass
	#Load meta - boneCount/materialCount/triangleCount
	def loadmeta(self,bs):
		self.meta.append(bs.readInt())
		self.meta.append(bs.readInt())
		self.meta.append(bs.readInt())	
		#print("meta:")
		#print(self.meta)	
	#Load bones - pos/rot/scale
	def loadBones(self, bs):
		sectionID = bs.readUInt()
		boneCount = bs.readUInt()
		for i in range(0, boneCount):
			boneID = bs.readInt()
			boneParent = bs.readInt()
			BonePos = NoeVec3.fromBytes(bs.readBytes(12))
			BoneRot = NoeQuat.fromBytes(bs.readBytes(16))
			BoneScale = NoeVec3.fromBytes(bs.readBytes(12))
			#make matrix
			boneMtx = BoneRot.toMat43().inverse()
			boneMtx[3] = BonePos
			boneName = bs.readString()
			self.alignPosition(bs, 4)
			instanceBone = NoeBone(i, boneName, boneMtx, None, boneParent)
			self.boneList.append(instanceBone)
			#print("bone:")
			#print("id: " + str(boneID) + " name: " + boneName + " parentIX: " + str(boneParent))
		self.boneList = rapi.multiplyBones(self.boneList)
	#Load materials - mat id/index	
	def loadMaterialList(self, bs):
		sectionID = bs.readUInt()
		matCount = bs.readUInt()		
		for i in range(0, matCount):
			m_id = bs.readInt()
			m_name = bs.readString()
			self.alignPosition(bs, 4)			
			self.matList.append([m_id,m_name])
			#print("material:")
			#print("id: " + str(m_id) + " name: " + m_name)		
	def loadTriangleList(self, bs):
		sectionID = bs.readUInt()
		triCount = bs.readUInt()
		#first make a fake index array(not sure if this is the right way)
		fbo = bytearray()
		for ir in range(0,(triCount - 1)):
			fbo.extend(bytearray(struct.pack('<i',0 + ir)))
			fbo.extend(bytearray(struct.pack('<i',1 + ir)))
			fbo.extend(bytearray(struct.pack('<i',2 + ir)))			
			#combine these (fucken python seriously -_-)		
			#fbo.append(0 + ir)
			#fbo.append(1 + ir)
			#fbo.append(2 + ir)
		#print(hex(fbo[260]))
		#for pv in range(0,len(fbo) - 200):
		#	print(hex(fbo[pv]))
		#triangle buffer object (contains matIndex + 3 verts)
		tbo = []
		for i in range(0, triCount):
			mat_index = bs.readInt()
			triElemPos = []
			triElemNor = []
			triElemUV = []
			triElemBL = []
			triElemBW = []
			#generate buffer content
			for trx in range(0,3):
				#position
				vertPos_X = bs.readFloat()
				vertPos_Y = bs.readFloat()
				vertPos_Z = bs.readFloat()
				triElemPos.append(vertPos_X)
				triElemPos.append(vertPos_Y)
				triElemPos.append(vertPos_Z)
				#normal
				vertNor_X = bs.readFloat()
				vertNor_Y = bs.readFloat()
				vertNor_Z = bs.readFloat()
				triElemNor.append(vertNor_X)
				triElemNor.append(vertNor_Y)
				triElemNor.append(vertNor_Z)				
				#uv
				vertUV_X = bs.readFloat()
				vertUV_Y = bs.readFloat()
				triElemUV.append(vertUV_X)
				triElemUV.append(vertUV_Y)						
				#read boneLinks
				NumOfBoneLinks = bs.readInt()
				for j in range(0,NumOfBoneLinks):
					triElemBL.append(bs.readInt())
					triElemBW.append(bs.readFloat())

				#check if extra append is needed
				if NumOfBoneLinks == 4:
					pass
				elif NumOfBoneLinks == 3:
					for bx in range(0,1):
						triElemBL.append(0)
						triElemBW.append(0)
				elif NumOfBoneLinks == 2:
					for bx in range(0,2):	
						triElemBL.append(0)
						triElemBW.append(0)
				elif NumOfBoneLinks == 1:
					for bx in range(0,3):	
						triElemBL.append(0)
						triElemBW.append(0)
				elif NumOfBoneLinks == 0:
					for bx in range(0,4):
						triElemBL.append(0)
						triElemBW.append(0)
				else:
					noesis.doException("This value should always be something inrange 0 to 4 got a value of " + str(NumOfBoneLinks))
				
			#check our data?
			#for ic in range(0,len(triElemPos)):
			#print("len of POSXYZ: " + str(len(triElemPos)))
		
			#pack up to bytearray
			vertBuff = bytes()
			normBuff = bytes()
			uvBuff = bytes()
			idxBuff = bytes()
			bwxBuff = bytes()
			
			vertBuff = struct.pack("<" + 'f'*len(triElemPos), *triElemPos)
			normBuff = struct.pack("<" + 'f'*len(triElemNor), *triElemNor)
			uvBuff = struct.pack("<" + 'f'*len(triElemUV), *triElemUV)
			idxBuff = struct.pack("<" + 'i'*len(triElemBL), *triElemBL)
			bwxBuff = struct.pack("<" + 'f'*len(triElemBW), *triElemBW)
			#finally bind our arrays to rapi
			rapi.rpgBindPositionBuffer(vertBuff, noesis.RPGEODATA_FLOAT, 12)
			rapi.rpgBindNormalBuffer(normBuff, noesis.RPGEODATA_FLOAT, 12)
			rapi.rpgBindUV1Buffer(uvBuff, noesis.RPGEODATA_FLOAT, 8)
			rapi.rpgBindBoneIndexBufferOfs(idxBuff,noesis.RPGEODATA_INT,16,0,4)
			rapi.rpgBindBoneWeightBufferOfs(bwxBuff,noesis.RPGEODATA_FLOAT,16,0,4)		
			#rapi.rpgBindPositionBufferOfs(triElemBuffer, noesis.RPGEODATA_FLOAT, 32, 0)
			#rapi.rpgBindNormalBufferOfs(triElemBuffer, noesis.RPGEODATA_FLOAT, 32, 12)
			#rapi.rpgBindUV1BufferOfs(triElemBuffer, noesis.RPGEODATA_FLOAT, 32, 24)
			#rapi.rpgBindBoneIndexBufferOfs(triElemBuffer, noesis.RPGEODATA_INT, 32, 0, 4)
			#rapi.rpgBindBoneWeightBufferOfs(triElemBuffer, noesis.RPGEODATA_FLOAT, 48, 0, 4)
			rapi.rpgSetMaterial(self.matList[mat_index][1])
			#rapi.rpgCommitTriangles(None, noesis.RPGEODATA_FLOAT, 1, noesis.RPGEO_POINTS, 1)	
			rapi.rpgCommitTriangles(None, noesis.RPGEODATA_FLOAT, 3, noesis.RPGEO_TRIANGLE, 1)
	def loadUnk1(self, bs):
		pass

	def loadBonePallet(self, bs):
		pass

	def loadTex(self): 
		pass

	def loadMatInfo(self, bs):
		pass

	def loadMeshs(self, bs):
		pass

def bmdLoadModel(data, mdlList):
	ctx = rapi.rpgCreateContext()
	bmd = bmdFile(NoeBitStream(data))
	bmd.loadAll(bmd.bs)
	#rapi.rpgSmoothNormals()
	#rapi.rpgSmoothTangents()
	#rapi.rpgUnifyBinormals(1)	
	try:
		mdl = rapi.rpgConstructModel()
	except:
		mdl = NoeModel()
	#mdl.setModelMaterials(NoeModelMaterials(bmd.texList, bmd.matList))
	mdlList.append(mdl); mdl.setBones(bmd.boneList)	
	return 1
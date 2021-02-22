//*****************
//* BMD (Binary Model Data)
//* Author : Cra0kalo
//* Website: http://cra0kalo.com
//* Date: 2014
//*****************


//****Notes****
// BMD(Binary Model Data) is a format I've created which is derived from Valve's SMD(Studiomdl Data).
// It has many new features and changes and as the name hints at it, its a binary format much like DMX.

//Initial Structure Ideas?
//-SMD like bonelist
//-Can contain multiple mesh pieces
//-Stores mesh data in triangles
//-Has a material list too
//-Has extraInfo list for meta data


//****File Format****


//*Header nothing special
typedef struct
{
    string	signature;		//BMDC
    int32	version;
    int32	unused;		
    int32 	filesize;
} BMDHeader; //header of file


//*Format metadata
typedef struct
{
    int32	boneCount;
    int32	materialCount;	
    int32 	triangleCount;
} BMDmeta; 



//*BoneList
uint32	sectionID;
uint32 	boneCount;
typedef struct
{
	int32	b_id;
	int32	b_parentIndex;
	vec3	b_pos;
	quat4	b_rot;
	vec3	b_scale;
	asciiz	b_name;	//note aligned to 4bytes
} t_bonelist; 



//*MaterialList
uint32	sectionID;
uint32 	matCount;
typedef struct
{
	int32	m_id;
	asciiz	m_name;	//note aligned to 4bytes
} t_matlist; 



//*TriangleList
uint32	sectionID;
uint32 	triCount;
typedef struct
{	
	int32	matIndex;
	triVert	A;	//Vert A of triangle
	triVert	B;	//Vert B of triangle
	triVert C;	//Vert C of triangle
	
} t_trilist; 


typedef struct
{	
	vec3	t_pos;	//position XYZ
	vec3	t_nor;	//normals
	vec2	t_uv;	//uvs
	int32	NumOfBoneLinks;	
		for(int i = 0; i < NumOfBoneLinks;i++)
		{
			int32	dcl_blendindice;
			float	dcl_blendweight;	
		}	
} triVert; 


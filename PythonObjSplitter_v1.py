#python obj splitter
import sys
import math

k_subdivisionCount = 10

def getVertsOrUvsForGivenTriangle(triangleID, vertsOrUvsArray):
	data = []
	for i in range(0,3):
		vuvIndex = triangleID * 3 + i
		data.append(vertsOrUvsArray[vuvIndex])
	return data

def generateTriangleLineFromID(triangleID):
	triangleString = "f"
	for i in range(0,3):
		indice = 1 + triangleID * 3 + i
		triangleString += " " + str(indice) + "/" + str(indice)
	return triangleString



print("testing")
objFilename = sys.argv[1]
print(objFilename)

objFile = open(objFilename)
#print( len(objFile.readlines()) )

headerstring = []

verticesList = []
uvsList = []
trianglesList = []

for line in objFile:
	splitLine = line.strip().split(' ')
	if splitLine[0] == 'v' :
		verticesList.append(line.strip())
	elif splitLine[0] == 'vt' :
		uvsList.append(line.strip())
	elif splitLine[0] == 'f' :
		trianglesList.append(line.strip())
	else:
		headerstring.append(line.strip())


print("vertices: " + str(len(verticesList)))
print("uvs: " + str(len(uvsList)))
print("triangles: " + str(len(trianglesList)))
print("header: " + str(headerstring))

# triangles count: 198548
# vertices count: 595644

# 198548/10 = 19854
# 19854 * 9  = 178686
# 198540 - 178686 = 19862

totalTriangles = len(trianglesList)
trianglesPerMesh_MainBatch = int(math.floor(totalTriangles/k_subdivisionCount))  #19854
trainglesPerMesh_LastMesh = int(totalTriangles - ( trianglesPerMesh_MainBatch * (k_subdivisionCount-1) ))  #19862
vertexCounter = 0;

print("------------------")
print("Subdivision count: " + str(k_subdivisionCount))
print("triangles per mesh Main Batch: " + str(trianglesPerMesh_MainBatch))
print("triangles per mesh Last Mesh: " + str(trainglesPerMesh_LastMesh))
print("------------------")

triangleCounter = 0
for i in range(0,10):
	verts = []
	uvs = []
	tris = []
	print("////////////////")
	filename = objFilename.strip(".obj") + "_" + str(i) + ".obj"
	print("starting " + filename)

	trianglesCount = trianglesPerMesh_MainBatch
	if (i == 9):
		trianglesCount = trainglesPerMesh_LastMesh

	localFileTriangleCounter = 0

	# ittereate through triangles and add according vertices and uvs to the lists
	for j in range(0, trianglesCount):
		verts.extend(getVertsOrUvsForGivenTriangle(triangleCounter, verticesList))
		uvs.extend(getVertsOrUvsForGivenTriangle(triangleCounter, uvsList))
		tris.append(generateTriangleLineFromID(localFileTriangleCounter))
		triangleCounter += 1
		localFileTriangleCounter += 1
	

	newFile = open(filename, 'w')
	newFile.writelines( '\n'.join(headerstring) )
	newFile.write('\n')
	newFile.writelines( '\n'.join(verts) )
	newFile.write('\n')
	newFile.writelines( '\n'.join(uvs) )	
	newFile.write('\n')
	newFile.writelines( '\n'.join(tris) )
	newFile.close()

	print("verts: " + str(len(verts)))
	print("uvs: " + str(len(uvs)))
	print("tris: " + str(len(tris)))

	print("finished: " + filename)

print("+++++++++++++++++++++")
print("PROGRAM COMPLETE")


objFile.close();

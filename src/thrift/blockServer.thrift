include "shared.thrift"

namespace cpp blockServer
namespace py blockServer
namespace java blockServer


typedef shared.response response

struct hashBlock {
	1: string hash,
	2: binary block,
	3: string status
}

struct hashBlocks {
	1: list<hashBlock> blocks
}

service BlockServerService {
	response storeBlock(1: hashBlock hashblock),
	hashBlock getBlock(1: string hash),
	response deleteBlock(1: string hash)
 	i64 getNum()
	bool hasBlock(1: string hash)

}

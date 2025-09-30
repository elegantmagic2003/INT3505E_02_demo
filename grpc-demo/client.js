import grpc from "@grpc/grpc-js";
import protoLoader from "@grpc/proto-loader";

const PROTO_PATH = "./helloworld.proto";
const packageDef = protoLoader.loadSync(PROTO_PATH, {});
const grpcObject = grpc.loadPackageDefinition(packageDef);
const Greeter = grpcObject.helloworld.Greeter;

// Connect to server
const client = new Greeter("localhost:50051", grpc.credentials.createInsecure());

// Gọi hàm remote
client.SayHello({ name: "Alice" }, (err, response) => {
  if (err) {
    console.error(err);
    return;
  }
  console.log("✅ Server replied:", response.message);
});

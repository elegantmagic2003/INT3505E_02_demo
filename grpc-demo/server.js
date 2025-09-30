import grpc from "@grpc/grpc-js";
import protoLoader from "@grpc/proto-loader";

// Load proto file
const PROTO_PATH = "./helloworld.proto";
const packageDef = protoLoader.loadSync(PROTO_PATH, {});
const grpcObject = grpc.loadPackageDefinition(packageDef);
const greeter = grpcObject.helloworld.Greeter;

// Implement service
function sayHello(call, callback) {
  callback(null, { message: "Hello " + call.request.name });
}

// Start server
function main() {
  const server = new grpc.Server();
  server.addService(greeter.service, { SayHello: sayHello });
  server.bindAsync(
    "0.0.0.0:50051",
    grpc.ServerCredentials.createInsecure(),
    () => {
      console.log("🚀 gRPC server running at http://0.0.0.0:50051");
      server.start();
    }
  );
}

main();

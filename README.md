# Demo of Service/Client API Design
This project combines gRPC, FastAPI, and React.

## fastAPI with React
- Debugging using Postman through VS Code.
- FastAPI to define endpoints under 'inventory' directory
- redis cloud database (app.redislabs.com) hosted on Google Cloud Platform


After the inventory and payment microservices are ready we create their REACT frontend by calling:
```
npx create-react-app inventory-frontend
```

Note: this is using the instructions https://www.youtube.com/watch?v=Cy9fAvsXGZA


## gRPC server - client in python
    Mostly following the Quickstart from https://grpc.io/docs/languages/python/quickstart/.
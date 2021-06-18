# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import banking_pb2 as banking__pb2


class BankingStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateAccount = channel.unary_unary(
                '/Banking/CreateAccount',
                request_serializer=banking__pb2.CreateRequest.SerializeToString,
                response_deserializer=banking__pb2.CreateReply.FromString,
                )
        self.Add = channel.unary_unary(
                '/Banking/Add',
                request_serializer=banking__pb2.AddRequest.SerializeToString,
                response_deserializer=banking__pb2.AddReply.FromString,
                )
        self.AddWOReturn = channel.unary_unary(
                '/Banking/AddWOReturn',
                request_serializer=banking__pb2.AddWORequest.SerializeToString,
                response_deserializer=banking__pb2.AddWOReply.FromString,
                )
        self.Sub = channel.unary_unary(
                '/Banking/Sub',
                request_serializer=banking__pb2.SubRequest.SerializeToString,
                response_deserializer=banking__pb2.SubReply.FromString,
                )


class BankingServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateAccount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Add(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddWOReturn(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Sub(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BankingServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateAccount,
                    request_deserializer=banking__pb2.CreateRequest.FromString,
                    response_serializer=banking__pb2.CreateReply.SerializeToString,
            ),
            'Add': grpc.unary_unary_rpc_method_handler(
                    servicer.Add,
                    request_deserializer=banking__pb2.AddRequest.FromString,
                    response_serializer=banking__pb2.AddReply.SerializeToString,
            ),
            'AddWOReturn': grpc.unary_unary_rpc_method_handler(
                    servicer.AddWOReturn,
                    request_deserializer=banking__pb2.AddWORequest.FromString,
                    response_serializer=banking__pb2.AddWOReply.SerializeToString,
            ),
            'Sub': grpc.unary_unary_rpc_method_handler(
                    servicer.Sub,
                    request_deserializer=banking__pb2.SubRequest.FromString,
                    response_serializer=banking__pb2.SubReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Banking', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Banking(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Banking/CreateAccount',
            banking__pb2.CreateRequest.SerializeToString,
            banking__pb2.CreateReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Add(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Banking/Add',
            banking__pb2.AddRequest.SerializeToString,
            banking__pb2.AddReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddWOReturn(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Banking/AddWOReturn',
            banking__pb2.AddWORequest.SerializeToString,
            banking__pb2.AddWOReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Sub(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Banking/Sub',
            banking__pb2.SubRequest.SerializeToString,
            banking__pb2.SubReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

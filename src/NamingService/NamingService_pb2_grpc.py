# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import src.NamingService.NamingService_pb2 as NamingService__pb2


class NamingServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.add_ = channel.unary_unary(
                '/NamingService/add_',
                request_serializer=NamingService__pb2.AddRequest.SerializeToString,
                response_deserializer=NamingService__pb2.AddReply.FromString,
                )
        self.get_ = channel.unary_unary(
                '/NamingService/get_',
                request_serializer=NamingService__pb2.GetRequest.SerializeToString,
                response_deserializer=NamingService__pb2.GetReply.FromString,
                )
        self.get_random_ = channel.unary_unary(
                '/NamingService/get_random_',
                request_serializer=NamingService__pb2.GetRandomRequest.SerializeToString,
                response_deserializer=NamingService__pb2.GetRandomReply.FromString,
                )
        self.get_all_ = channel.unary_stream(
                '/NamingService/get_all_',
                request_serializer=NamingService__pb2.GetAllRequest.SerializeToString,
                response_deserializer=NamingService__pb2.GetAllReply.FromString,
                )
        self.delete_ = channel.unary_unary(
                '/NamingService/delete_',
                request_serializer=NamingService__pb2.DeleteRequest.SerializeToString,
                response_deserializer=NamingService__pb2.DeleteReply.FromString,
                )
        self.delete_all_ = channel.unary_unary(
                '/NamingService/delete_all_',
                request_serializer=NamingService__pb2.DeleteAllRequest.SerializeToString,
                response_deserializer=NamingService__pb2.DeleteAllReply.FromString,
                )


class NamingServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def add_(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_random_(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_all_(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete_(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete_all_(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NamingServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'add_': grpc.unary_unary_rpc_method_handler(
                    servicer.add_,
                    request_deserializer=NamingService__pb2.AddRequest.FromString,
                    response_serializer=NamingService__pb2.AddReply.SerializeToString,
            ),
            'get_': grpc.unary_unary_rpc_method_handler(
                    servicer.get_,
                    request_deserializer=NamingService__pb2.GetRequest.FromString,
                    response_serializer=NamingService__pb2.GetReply.SerializeToString,
            ),
            'get_random_': grpc.unary_unary_rpc_method_handler(
                    servicer.get_random_,
                    request_deserializer=NamingService__pb2.GetRandomRequest.FromString,
                    response_serializer=NamingService__pb2.GetRandomReply.SerializeToString,
            ),
            'get_all_': grpc.unary_stream_rpc_method_handler(
                    servicer.get_all_,
                    request_deserializer=NamingService__pb2.GetAllRequest.FromString,
                    response_serializer=NamingService__pb2.GetAllReply.SerializeToString,
            ),
            'delete_': grpc.unary_unary_rpc_method_handler(
                    servicer.delete_,
                    request_deserializer=NamingService__pb2.DeleteRequest.FromString,
                    response_serializer=NamingService__pb2.DeleteReply.SerializeToString,
            ),
            'delete_all_': grpc.unary_unary_rpc_method_handler(
                    servicer.delete_all_,
                    request_deserializer=NamingService__pb2.DeleteAllRequest.FromString,
                    response_serializer=NamingService__pb2.DeleteAllReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'NamingService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class NamingService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def add_(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/NamingService/add_',
            NamingService__pb2.AddRequest.SerializeToString,
            NamingService__pb2.AddReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/NamingService/get_',
            NamingService__pb2.GetRequest.SerializeToString,
            NamingService__pb2.GetReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_random_(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/NamingService/get_random_',
            NamingService__pb2.GetRandomRequest.SerializeToString,
            NamingService__pb2.GetRandomReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_all_(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/NamingService/get_all_',
            NamingService__pb2.GetAllRequest.SerializeToString,
            NamingService__pb2.GetAllReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def delete_(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/NamingService/delete_',
            NamingService__pb2.DeleteRequest.SerializeToString,
            NamingService__pb2.DeleteReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def delete_all_(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/NamingService/delete_all_',
            NamingService__pb2.DeleteAllRequest.SerializeToString,
            NamingService__pb2.DeleteAllReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

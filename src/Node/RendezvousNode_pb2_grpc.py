# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import src.Node.RendezvousNode_pb2 as RendezvousNode__pb2


class RendezvousNodeStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.get_request = channel.unary_unary(
                '/RendezvousNode/get_request',
                request_serializer=RendezvousNode__pb2.NodeGetRequest.SerializeToString,
                response_deserializer=RendezvousNode__pb2.NodeGetReply.FromString,
                )
        self.get_objects = channel.unary_stream(
                '/RendezvousNode/get_objects',
                request_serializer=RendezvousNode__pb2.NodeEmpty.SerializeToString,
                response_deserializer=RendezvousNode__pb2.NodeGetObjectsReply.FromString,
                )
        self.get_replicas = channel.unary_stream(
                '/RendezvousNode/get_replicas',
                request_serializer=RendezvousNode__pb2.NodeEmpty.SerializeToString,
                response_deserializer=RendezvousNode__pb2.NodeGetReplicasReply.FromString,
                )
        self.inspect_lost_entries = channel.unary_unary(
                '/RendezvousNode/inspect_lost_entries',
                request_serializer=RendezvousNode__pb2.NodeGetLostEntriesRequest.SerializeToString,
                response_deserializer=RendezvousNode__pb2.NodeEmpty.FromString,
                )
        self.hash_value_for_key = channel.unary_unary(
                '/RendezvousNode/hash_value_for_key',
                request_serializer=RendezvousNode__pb2.NodeHashValueForRequest.SerializeToString,
                response_deserializer=RendezvousNode__pb2.NodeHashValueForReply.FromString,
                )
        self.send_item_to_new_node = channel.unary_unary(
                '/RendezvousNode/send_item_to_new_node',
                request_serializer=RendezvousNode__pb2.NodeSendItemToNewNodeRequest.SerializeToString,
                response_deserializer=RendezvousNode__pb2.NodeEmpty.FromString,
                )
        self.remove_all = channel.unary_unary(
                '/RendezvousNode/remove_all',
                request_serializer=RendezvousNode__pb2.NodeEmpty.SerializeToString,
                response_deserializer=RendezvousNode__pb2.NodeEmpty.FromString,
                )


class RendezvousNodeServicer(object):
    """Missing associated documentation comment in .proto file."""

    def get_request(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_objects(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_replicas(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def inspect_lost_entries(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def hash_value_for_key(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def send_item_to_new_node(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def remove_all(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RendezvousNodeServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'get_request': grpc.unary_unary_rpc_method_handler(
                    servicer.get_request,
                    request_deserializer=RendezvousNode__pb2.NodeGetRequest.FromString,
                    response_serializer=RendezvousNode__pb2.NodeGetReply.SerializeToString,
            ),
            'get_objects': grpc.unary_stream_rpc_method_handler(
                    servicer.get_objects,
                    request_deserializer=RendezvousNode__pb2.NodeEmpty.FromString,
                    response_serializer=RendezvousNode__pb2.NodeGetObjectsReply.SerializeToString,
            ),
            'get_replicas': grpc.unary_stream_rpc_method_handler(
                    servicer.get_replicas,
                    request_deserializer=RendezvousNode__pb2.NodeEmpty.FromString,
                    response_serializer=RendezvousNode__pb2.NodeGetReplicasReply.SerializeToString,
            ),
            'inspect_lost_entries': grpc.unary_unary_rpc_method_handler(
                    servicer.inspect_lost_entries,
                    request_deserializer=RendezvousNode__pb2.NodeGetLostEntriesRequest.FromString,
                    response_serializer=RendezvousNode__pb2.NodeEmpty.SerializeToString,
            ),
            'hash_value_for_key': grpc.unary_unary_rpc_method_handler(
                    servicer.hash_value_for_key,
                    request_deserializer=RendezvousNode__pb2.NodeHashValueForRequest.FromString,
                    response_serializer=RendezvousNode__pb2.NodeHashValueForReply.SerializeToString,
            ),
            'send_item_to_new_node': grpc.unary_unary_rpc_method_handler(
                    servicer.send_item_to_new_node,
                    request_deserializer=RendezvousNode__pb2.NodeSendItemToNewNodeRequest.FromString,
                    response_serializer=RendezvousNode__pb2.NodeEmpty.SerializeToString,
            ),
            'remove_all': grpc.unary_unary_rpc_method_handler(
                    servicer.remove_all,
                    request_deserializer=RendezvousNode__pb2.NodeEmpty.FromString,
                    response_serializer=RendezvousNode__pb2.NodeEmpty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'RendezvousNode', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RendezvousNode(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def get_request(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RendezvousNode/get_request',
            RendezvousNode__pb2.NodeGetRequest.SerializeToString,
            RendezvousNode__pb2.NodeGetReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_objects(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/RendezvousNode/get_objects',
            RendezvousNode__pb2.NodeEmpty.SerializeToString,
            RendezvousNode__pb2.NodeGetObjectsReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_replicas(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/RendezvousNode/get_replicas',
            RendezvousNode__pb2.NodeEmpty.SerializeToString,
            RendezvousNode__pb2.NodeGetReplicasReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def inspect_lost_entries(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RendezvousNode/inspect_lost_entries',
            RendezvousNode__pb2.NodeGetLostEntriesRequest.SerializeToString,
            RendezvousNode__pb2.NodeEmpty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def hash_value_for_key(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RendezvousNode/hash_value_for_key',
            RendezvousNode__pb2.NodeHashValueForRequest.SerializeToString,
            RendezvousNode__pb2.NodeHashValueForReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def send_item_to_new_node(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RendezvousNode/send_item_to_new_node',
            RendezvousNode__pb2.NodeSendItemToNewNodeRequest.SerializeToString,
            RendezvousNode__pb2.NodeEmpty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def remove_all(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RendezvousNode/remove_all',
            RendezvousNode__pb2.NodeEmpty.SerializeToString,
            RendezvousNode__pb2.NodeEmpty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

import json

from tornado import gen, ioloop
from tchannel import TChannel, from_thrift_module
from tchannel.testing.data.generated.ThriftTest import ThriftTest


tchannel = TChannel('thrift-client')

service = from_thrift_module(
    service='thrift-server',
    thrift_module=ThriftTest,
    hostport='localhost:54497'
)


@gen.coroutine
def make_request():

    resp = yield tchannel.thrift(
        request=service.testString(thing="req"),
        headers={
            'req': 'header',
        },
    )

    raise gen.Return(resp)


resp = ioloop.IOLoop.current().run_sync(make_request)

assert resp.headers == {
    'resp': 'header',
}
assert resp.body == 'resp'

print resp.body
print json.dumps(resp.headers)
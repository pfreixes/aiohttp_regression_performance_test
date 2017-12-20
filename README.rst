=======================================
Performance regression test for Aiohttp
=======================================

This tool allows the developer to run a simple benchmark for a set of specific Git references and see
empirically the evolution of the performance in Aiohttp_ during each Git reference

The Websever used uses `uvloop` and returns a simple string in a unique resource, as can be seen in the
following snippet:

.. code-block:: python

    async def handle(request):
        return web.Response(text='hellow world')

The client used is a simple Wrk_ execution having N connections and N threads accessing to that resource
within a limited lifespan, for example:

.. code-block:: bash

    wrk -c 20 -d 15 -t 20 http://127.0.0.1:5000


This comand is exeucted N times and the avg of the requests per second will be used as a final value for
a sepcific git reference for Aiohttp.

Results for the last 30 commits in master
=========================================

Foundations of v3

[97b9373f] Benchmark req/sec 8194
[c4efde83] Benchmark req/sec 8088
[6f955fbd] Benchmark req/sec 8287
[51961a7e] Benchmark req/sec 8164
[bd1c6178] Benchmark req/sec 8285
[9cc03cd5] Benchmark req/sec 8163
[4412fc92] Benchmark req/sec 8253
[486eaf2b] Benchmark req/sec 8227
[c178a99c] Benchmark req/sec 8161
[05a5a6c3] Benchmark req/sec 8194
[d02ca2ad] Benchmark req/sec 8084
[1cb4fa27] Benchmark req/sec 8136
[29e5eac3] Benchmark req/sec 8132
[b57caab2] Benchmark req/sec 8047
[c256c29a] Benchmark req/sec 8088
[dd234f33] Benchmark req/sec 8248
[76f92744] Benchmark req/sec 8243
[f0fe9230] Benchmark req/sec 8047
[245d3bf5] Benchmark req/sec 8186
[affbbd95] Benchmark req/sec 8210
[70546390] Benchmark req/sec 8124
[7e3f5551] Benchmark req/sec 8271


Results for the v2 version
==========================

[2.0.0] Benchmark req/sec 8910
[2.0.0rc1] Benchmark req/sec 9336
[2.0.1] Benchmark req/sec 9330
[2.0.2] Benchmark req/sec 9423
[2.0.3] Benchmark req/sec 9348
[2.0.3-1] Benchmark req/sec 9267
[2.0.4] Benchmark req/sec 9485
[2.0.5] Benchmark req/sec 9542
[2.0.6] Benchmark req/sec 9196
[2.0.7] Benchmark req/sec 9341
[v2.1.0] Benchmark req/sec 9453
[v2.2.0] Benchmark req/sec 9033
[v2.2.1] Benchmark req/sec 9531
[v2.2.2] Benchmark req/sec 9119
[v2.2.3] Benchmark req/sec 9169
[v2.2.4] Benchmark req/sec 9197
[v2.2.5] Benchmark req/sec 9136
[v2.3.0] Benchmark req/sec 9118
[v2.3.0a1] Benchmark req/sec 9042
[v2.3.0a2] Benchmark req/sec 8934
[v2.3.0a3] Benchmark req/sec 9096
[v2.3.0a4] Benchmark req/sec 8860
[v2.3.1] Benchmark req/sec 8892 **Performance degradation**
[v2.3.1a1] Benchmark req/sec 9013
[v2.3.2] Benchmark req/sec 9226
[v2.3.2b1] Benchmark req/sec 8958
[v2.3.2b2] Benchmark req/sec 9011
[v2.3.2b3] Benchmark req/sec 8954
[v2.3.3] Benchmark req/sec 8929
[v2.3.4] Benchmark req/sec 8979
[v2.3.5] Benchmark req/sec 8832
[v2.3.6] Benchmark req/sec 8108 **Performance degradation**

Results for the v1 version
==========================

Legacy, just for documentation

[1.3.1] Benchmark req/sec 5964
[1.3.2] Benchmark req/sec 5905
[1.3.3] Benchmark req/sec 6000
[1.3.4] Benchmark req/sec 5948
[1.3.5] Benchmark req/sec 6018

.. _Aiohttp: https://github.com/aio-libs/aiohttp
.. _Wrk: https://github.com/wg/wrk

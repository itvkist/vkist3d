import traceback
import aiohttp_cors

from aiohttp import web
from sfm import generate_dense_point_cloud, generate_texture, reconstruct

app = web.Application(client_max_size=200*1024**2)
cors = aiohttp_cors.setup(app)

# server
def create_error_middleware(overrides):
    @web.middleware
    async def error_middleware(request, handler):
        try:
            resp = await handler(request)
            return resp
        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                resp = await override(request, ex)
                resp.set_status(ex.status)
                return resp
        except Exception as e:
            print(traceback.format_exc())
            resp = await overrides[500](request, web.HTTPError(text=traceback.format_exc()))
            resp.set_status(500)
            return resp

    return error_middleware

async def handle_403(request, ex):
    # return web.json_response({"result": {'message': ex.text}}, status=403)
    raise web.HTTPFound(location='./')


async def handle_404(request, ex):
    # return web.json_response({"result": {'message': ex.text}}, status=404)
    raise web.HTTPFound(location='./')


async def handle_500(request, ex):
    # return web.json_response({"result": {'message': ex.text}}, status=500)
    raise web.HTTPFound(location='./')


def setup_middlewares(app):
    error_middleware = create_error_middleware({
        403: handle_403,
        404: handle_404,
        500: handle_500,
    })
    app.middlewares.append(error_middleware)

setup_middlewares(app)

# generate dense point cloud
async def dense(request):
    data = await request.json()
    path = data['path']
    result = generate_dense_point_cloud(path)
    return web.Response(text=result)

#generate mesh and texture
async def texture(request):
    data = await request.json()
    path = data['path']
    result = generate_texture(path)
    return web.Response(text=result)

#generate all
async def reconstruction(request):
    data = await request.json()
    path = data['path']
    print(path)

    print('Generating point cloud')
    result1 = generate_dense_point_cloud(path)
    print(result1)

    print('Reconstructing mesh and texture')
    result2 = generate_texture(path)
    print('Finished reconstructing mesh at ' + result2)
    
    return web.Response(text=result2)

app.router.add_route('POST','/dense', dense, name="dense_reconstruction")

app.router.add_route('POST','/texture', texture, name="texture_reconstruction")

# app.router.add_route('POST','/reconstruct', reconstruction, name="reconstruction")

resource = cors.add(app.router.add_resource("/reconstruct"))
route = cors.add(
    resource.add_route("POST", reconstruction), {
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })


if __name__=="__main__":
    web.run_app(app, port=7000)
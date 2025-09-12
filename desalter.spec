import os
import sys
from pathlib import Path

# Get the project root directory
project_root = Path(SPEC).parent

# Define the analysis
a = Analysis(
    ['launcher.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # Include frontend files
        (str(project_root / 'frontend'), 'frontend'),
        # Include backend files
        (str(project_root / 'backend'), 'backend'),
    ],
    hiddenimports=[
        # Core FastAPI and Uvicorn
        'fastapi',
        'fastapi.applications',
        'fastapi.routing',
        'fastapi.responses',
        'fastapi.staticfiles',
        'uvicorn',
        'uvicorn.main',
        'uvicorn.config',
        'uvicorn.server',
        'uvicorn.supervisors',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.websockets',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'uvicorn.logging',
        'uvicorn.run',
        'uvicorn.workers',
        'uvicorn.importer',

        # Starlette
        'starlette',
        'starlette.applications',
        'starlette.responses',
        'starlette.staticfiles',
        'starlette.routing',
        'starlette.endpoints',
        'starlette.middleware',
        'starlette.middleware.base',
        'starlette.middleware.cors',
        'starlette.middleware.trustedhost',
        'starlette.requests',
        'starlette.responses',
        'starlette.templating',
        'starlette.websockets',
        'starlette.background',
        'starlette.concurrency',
        'starlette.datastructures',
        'starlette.exceptions',
        'starlette.formparsers',
        'starlette.types',

        # Pydantic
        'pydantic',
        'pydantic.main',
        'pydantic.fields',
        'pydantic.validators',
        'pydantic.types',
        'pydantic.networks',
        'pydantic.color',
        'pydantic.datetime_parse',
        'pydantic.error_wrappers',
        'pydantic.errors',
        'pydantic.json',
        'pydantic.parse_obj_as',
        'pydantic.schema',
        'pydantic.tools',
        'pydantic.typing',
        'pydantic.utils',
        'pydantic.version',
        'pydantic.class_validators',
        'pydantic.config',
        'pydantic.dataclasses',
        'pydantic.env_settings',
        'pydantic.generics',
        'pydantic.main',
        'pydantic.parse',
        'pydantic.typing',

        # Uvicorn internals
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.loops.uvloop',
        'uvicorn.loops.asyncio',
        'uvicorn.middleware',
        'uvicorn.middleware.proxy_headers',
        'uvicorn.middleware.wsgi',

        # Other dependencies
        'backend.main',
        'webbrowser',
        'pathlib',
        'pathlib.Path',
        'typing',
        'typing_extensions',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='desalter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

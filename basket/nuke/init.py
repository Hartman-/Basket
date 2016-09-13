def setupDefault():
    # DEFINE EXAMPLE ENVIRONMENT
    os.environ['SHOW'] = 'PROJ_local'
    os.environ['SEQ'] = 'xyz'
    os.environ['SHOT'] = '010'

if os.getenv('SEQ') is None or os.getenv('SHOT') is None or os.getenv('SHOW') is None:
    setupDefault()



def setupDefault():
    # DEFINE EXAMPLE ENVIRONMENT
    os.environ['SEQ'] = 'abc'
    os.environ['SHOT'] = '010'

if os.getenv('SEQ') is None or os.getenv('SHOT') is None:
    setupDefault()



import subprocess,os.path,os,sys

def basicSimulator():
    # Run a Python script
    # Use Popen to avoid hanging the main thread
    subprocess.Popen([sys.executable, os.path.join(
        os.path.dirname(__file__),
        "main_files",
        "basic_simulator",
        "main.py"
    )])

def cameraSimulator():
    # Run a Python script
    subprocess.Popen([sys.executable, os.path.join(
        os.path.dirname(__file__),
        "main_files",
        "camera_simulation",
        "camera.py"
    )])

def planetSimulator():
    # Run a Python script
    subprocess.Popen([sys.executable, os.path.join(
        os.path.dirname(__file__),
        "main_files",
        "planetary_motion",
        "planet.py"
    )])

def playgroundSimulator():
    # Run a Python script
    subprocess.Popen([sys.executable, os.path.join(
        os.path.dirname(__file__),
        "main_files",
        "drawable_shapes",
        "playground.py"
    )])

def pendulumSimulator():
    # Run a Python script
    subprocess.Popen([sys.executable, os.path.join(
        os.path.dirname(__file__),
        "main_files",
        "pendulum",
        "pendulum.py"
    )])

def atwoodMacSimulator():
    # Run a Python script
    subprocess.Popen([sys.executable,os.path.join(
        os.path.dirname(__file__),
        "main_files",
        "atwoods",
        "Atwoods.py"
    )])

def collisionSimulator():
    subprocess.Popen([sys.executable, os.path.join(
        os.path.dirname(__file__),
        "main_files",
        "collisions",
        "elasticCollision.py"
    )])

def secondcollisionSimulator():
    subprocess.Popen([sys.executable,os.path.join(
        os.path.dirname(__file__),
        "main_files",
        "collisions",
        "inelasticCollision.py"
    )])

def rotationalMotionSimulator():
    subprocess.Popen([sys.executable, os.path.join(
        os.path.dirname(__file__),
        "main_files",
        "rotational_motion",
        "RotationalMotion.py"
    )])

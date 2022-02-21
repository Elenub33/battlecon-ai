SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

python -m unittest discover $SCRIPT_DIR/test 2> test_results.txt
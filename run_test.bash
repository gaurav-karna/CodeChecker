echo "Running Capital One Assessment Test..."

echo "AUTHOR - Gaurav K. Karna | Copyright Gaurav K. Karna 2019" > test_output.txt
echo "Capital One Assessment 2019 - Software Developer" >> test_output.txt
echo "###################################" >> test_output.txt
echo "" >> test_output.txt

echo "Testing input file starting with ." >> test_output.txt
echo "-+-+-+-+-+-PROGRAM OUTPUT-+-+-+-+-+-" >> test_output.txt
python3 main.py -f .tester >> test_output.txt
echo "-+-+-+-+-+-FILE CONTENT-+-+-+-+-+-" >> test_output.txt
cat .tester >> test_output.txt
echo "###################################" >> test_output.txt

echo "Testing input file with no extension" >> test_output.txt
echo "-+-+-+-+-+-PROGRAM OUTPUT-+-+-+-+-+-" >> test_output.txt
python3 main.py -f test >> test_output.txt
echo "-+-+-+-+-+-FILE CONTENT-+-+-+-+-+-" >> test_output.txt
cat test >> test_output.txt
echo "###################################" >> test_output.txt

echo "Testing input file with invalid extension" >> test_output.txt
echo "-+-+-+-+-+-PROGRAM OUTPUT-+-+-+-+-+-" >> test_output.txt
python3 main.py -f test.xe >> test_output.txt
echo "-+-+-+-+-+-FILE CONTENT-+-+-+-+-+-" >> test_output.txt
cat test.xe >> test_output.txt
echo "###################################" >> test_output.txt

echo "Testing Java/JS/TS/C/C++/Go/C# and other Slash-based comment syntax languages" >> test_output.txt
echo "-+-+-+-+-+-PROGRAM OUTPUT-+-+-+-+-+-" >> test_output.txt
python3 main.py -f java_test.java >> test_output.txt
echo "-+-+-+-+-+-FILE CONTENT-+-+-+-+-+-" >> test_output.txt
cat java_test.java >> test_output.txt
echo "###################################" >> test_output.txt

echo "Testing Python and other hash-based comment syntax lanugages" >> test_output.txt
echo "-+-+-+-+-+-PROGRAM OUTPUT-+-+-+-+-+-" >> test_output.txt
python3 main.py -f python_test.py >> test_output.txt
echo "-+-+-+-+-+-FILE CONTENT-+-+-+-+-+-" >> test_output.txt
cat python_test.py >> test_output.txt
echo "###################################" >> test_output.txt
echo "############END OF TEST############" >> test_output.txt

echo "Test Completed. Check results in test_output.txt"
git clone https://BorisGrechanichenko@github.com/BorisGrechanichenko/ElectricityController/
fullSourcePath=$(pwd)/ElectricityController

# copy the program
cd ElectricityController/Controller/version3
sourcePath=$(pwd)

cd /home/pi/Documents
mkdir Projects
cd Projects
mkdir Controller
controllerPath=$(pwd)/Controller
cp -rf $sourcePath/* $controllerPath
rm -rf $fullSourcePath

# add autorun script
cd ~
if grep -qF "python3 main.py" .bashrc
then
	echo "The autorun has already been set up"
else
	echo '' >> .bashrc
	echo 'cd '$controllerPath >> .bashrc
	echo 'python3 main.py' >> .bashrc
	echo 'cd -' >> .bashrc
	echo "Autorun set up successfully"
fi


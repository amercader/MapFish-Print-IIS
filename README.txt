MapFish Print Module controller for IIS
------------------------------------------------------------------------

These modules implement the MapFish print protocol and allow you to run
the MapFish print module on a IIS server configured with PyISAPIe.

Support and feedback:
	Adrià Mercader (amercadero@gmail.com) - http://amercader.net

Special thanks to:
    Seth Girvin (geographika@gmail.com) - http://geographika.co.uk

Requirements:
	* Python 2.5+
	* IIS 7.0 (Not tested under IIS 6.0)
	* PyISAPIe 1.1.0+
	* JDK 1.5+
	* MapFish print module JAR file
	
Install:
	1.	Compile the MapFish print module JAR file following these
		instructions:
		
		http://mapfish.org/doc/print/installation.html#compilation
		
		Copy the resulting JAR file in the directory of your choice.
	
	2.	Copy a YAML configuration file for the print service in the
		directory of your choice and edit it as needed. You can find
		samples in the 'samples' directory of the MapFish print module
		source downloaded in the previous point. For a full reference of
		the configuration options you can check the following page:
		
		http://mapfish.org/doc/print/configuration.html
			
	3.	Install and configure PyISAPIe. The most up-to-date instructions
		seem to be the ones described in the README file included with
		PyISAPIe. If you want to run a 64 bit version, have a look at
		this post:
		
		http://geographika.co.uk/compiling-a-64-bit-version-of-pyisapie
	
	4.	Copy the files contained in this package (Http and WWW modules
		and the printer.ini file) where the PyISAPIe DLL can find them.
		The easier choice is in the same folder as the DLL. . You may
		want to move Http and WWW, e.g to site-packages, but the
		printer.ini file must be located in the DLL directory.
		
	5.	Edit printer.ini to define the configuration options:
		-	Path to the compiled MapFish print module JAR file.
		-	Path to the YAML configuration file for the print service
		-	The temporary directory that will use the service to store
			the generated files. Please note that the user running the
			application on IIS must have full access to this directory 
			(i.e. write and delete files). If commented out in the 
			printer.ini file, the application will try to use the
			default OS temporary directory (the one	returned by 
			gettempdir())
	
	6.	Create a virtual directory in IIS, and add the PyISAPIe DLL as a
		Wildcard Script Map.
		
	7.	Restart ISS and visit the following URL:
	
		http://<your_server>/<virtual_dir>/info.json
		
		You should receive a JSON response with the capabilities of the
		printing service.

Resources:
    * MapFish print module home:
        http://www.mapfish.org/doc/print/

    * PyISAPIe home:
        http://pyisapie.sourceforge.net

License:
    This code is released under the GNU GENERAL PUBLIC LICENSE version 3
    (GPLv3). Please check the following URL for the full details of this
    license:

    http://www.gnu.org/licenses/gpl.html

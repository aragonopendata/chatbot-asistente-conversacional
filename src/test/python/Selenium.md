## Configuracion de los test en Iexplore y Firefox

### Configuracion de Agente de Windows

Se configura un nodo Jenkins en Windows
- Instalacion de java
- Se crea una carpeta llamada JENKINS
- Se instala comando que lanzara Jenkins https://git-scm.com/download/win
- descarga desde Jenkins la app de java en el agente e instalacion como servicio
para configurar selenium
- descarga de nuget y ejecutar nuget install Selenium.WebDriver -Version 3.141.0
https://dist.nuget.org/win-x86-commandline/latest/nuget.exe
- descarga el driver de Firefox para windows
- descarga el driver de Iexplore

- instalar python
- agregar en PATH :  la carpeta JENKINS, python, git , los driver

https://github-production-release-asset-2e65be.s3.amazonaws.com/25354393/f106b700-ec87-11e9-8493-8d21289b5a9a?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20191108%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20191108T104625Z&X-Amz-Expires=300&X-Amz-Signature=98c5979a063372cacc91f5bfbcf36f0838a1aad35c22fe5684208cefc74b0c77&X-Amz-SignedHeaders=host&actor_id=0&response-content-disposition=attachment%3B%20filename%3Dgeckodriver-v0.26.0-win32.zip&response-content-type=application%2Foctet-stream


pip instalar selenium
ejecutar el codigo

para el IE http://selenium-release.storage.googleapis.com/2.42/IEDriverServer_Win32_2.42.0.zip

IEDriverServer

browser = webdriver.Ie("c:\\JENKINS\\IEDriverServer.exe")

>>> from selenium import webdriver
>>> capabilities = webdriver.DesiredCapabilities().FIREFOX
>>> capabilities["marionette"] = False
>>> browser = webdriver.Firefox(capabilities=capabilities)



### Grabar los script que se lanzan en los navegadores
en chrome -> el pluging ->  Katalon Recorder -> exportar como python

en Firefox se puede realizar con el
se-ide-logo
Welcome to Selenium IDE!
Version 3.14.0


### Registrar en Windows el IEDriverServer.exe
ver https://github.com/seleniumhq/selenium-google-code-issue-archive/issues/6511


For IE 11 only, you will need to set a registry entry on the target computer so that
the driver can maintain a connection to the instance of Internet Explorer it creates.
For 32-bit Windows installations, the key you must examine in the registry editor is
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Internet Explorer\Main\FeatureControl\FEATURE_BFCACHE.
For 64-bit Windows installations, the key is HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Internet
Explorer\Main\FeatureControl\FEATURE_BFCACHE. Please note that the FEATURE_BFCACHE
subkey may or may not be present, and should be created if it is not present. Important:
Inside this key, create a DWORD value named iexplore.exe with the value of 0.

Here you need to specify DWORD value named iexplore.exe with the value of 0 has to
be set both for 64bit and 32 bit Windows.
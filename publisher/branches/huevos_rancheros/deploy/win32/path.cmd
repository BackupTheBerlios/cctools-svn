@echo off

rem Build Environment configuration for building Python Extensions on Win32
rem (currently tailored for NRY's build machine)
rem
rem see http://www.vrplumber.com/programming/mstoolkit/ for more details

rem Set PATH=c:\Program Files\Microsoft Visual C++ Toolkit 2003\bin;c:\Program Files\Microsoft Platform SDK\Bin;c:\python24;%PATH%
Set PATH=c:\Program Files\Microsoft Visual C++ Toolkit 2003\bin;c:\python24;%PATH%
Set INCLUDE=c:\Program Files\Microsoft Visual C++ Toolkit 2003\include;c:\Program Files\Microsoft Platform SDK\include;c:\python24\include;%INCLUDE%
Set LIB=C:\Program Files\Microsoft Visual Studio .NET 2003\Vc7\lib;c:\Program Files\Microsoft Visual C++ Toolkit 2003\lib;c:\Program Files\Microsoft Platform SDK\Lib;c:\python24\libs;%LIB%

echo Visit http://msdn.microsoft.com/visualc/using/documentation/default.aspx for
echo complete compiler documentation.
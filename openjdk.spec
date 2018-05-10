Name     : openjdk
Version  : 8
Release  : 30
URL      : http://localhost/cgit/projects/jdk8/snapshot/jdk8-openjdk-src-8u-162-b12.tar.gz
Source0  : http://localhost/cgit/projects/jdk8/snapshot/jdk8-openjdk-src-8u-162-b12.tar.gz
Summary  : No detailed summary available
Group    : Development/Tools
License  : GPL-2.0 Apache-2.0 BSD-2-Clause BSD-3-Clause BSD-4-Clause HPND ICU LGPL-2.1 Libpng MIT MPL-2.0-no-copyleft-exception SAX-PD Unicode-TOU W3C
Patch1   : disable-doclint-by-default.patch
Patch2   : build.patch
Patch3   : dizstore.patch
BuildRequires : openjdk
BuildRequires : openjdk-dev
BuildRequires : zip
BuildRequires : libX11-dev
BuildRequires : libXtst-dev
BuildRequires : libXt-dev
BuildRequires : libXrender-dev
BuildRequires : libXi-dev
BuildRequires : libXext-dev
BuildRequires : xproto-dev
BuildRequires : xextproto-dev
BuildRequires : kbproto-dev
BuildRequires : renderproto-dev
BuildRequires : inputproto-dev
BuildRequires : cups-dev
BuildRequires : freetype-dev
BuildRequires : alsa-lib-dev
BuildRequires : ccache
BuildRequires : ca-certs
BuildRequires : openssl-dev
BuildRequires : nss-dev
BuildRequires : glibc-bin
Requires : openjdk-lib
Requires : openjdk-bin
Requires : openjdk-doc

%description
OpenJDK (Open Java Development Kit) is a free and open source implementation of
the Java Platform, Standard Edition (Java SE).

%package bin
Summary: bin components for the openjdk package.
Group: Binaries
Requires : openjdk-lib

%description bin
bin components for the openjdk package.

%package doc
Summary: doc components for the openjdk package.
Group: Documentation

%description doc
doc components for the openjdk package.

%package dev
Summary: dev components for the openjdk package.
Group: Development
Requires : openjdk

%description dev
dev components for the openjdk package.

%package lib 
Summary: lib components for the openjdk package.
Group: Libraries 
Provides : libjli.so()(64bit)
Provides : libjli.so(SUNWprivate_1.1)(64bit)

%description lib
lib components for the openjdk package.

%prep
%setup -q -n jdk8-openjdk-src-8u-162-b12
%patch1 -p1
%patch2 -p1
%patch3 -p1
%build
CLR_TRUST_STORE=%{_builddir}/trust-store clrtrust generate
export CXXFLAGS="$CXXFLAGS -std=gnu++98 -Wno-error -fno-delete-null-pointer-checks -fno-guess-branch-probability"
export CXXFLAGS_JDK="$CXXFLAGS"
export SYSDEFS="$CXXFLAGS"
bash configure \
--with-boot-jdk=/usr/lib/jvm/java-1.8.0-openjdk \
--x-includes=/usr/include/ \
--x-libraries=/usr/lib64 \
--with-extra-cflags="-O3 $CFLAGS -g1" \
--with-extra-cxxflags="$CXXFLAGS -g1" \
--with-zlib=system \
--enable-unlimited-crypto \
--with-cacerts-file=%{_builddir}/trust-store/compat/ca-roots.keystore \
--prefix=%{buildroot}/usr/lib

%install
export CXXFLAGS="$CXXFLAGS -std=gnu++98 -Wno-error -fno-delete-null-pointer-checks -fno-guess-branch-probability"
export CXXFLAGS_JDK="$CXXFLAGS"
export SYSDEFS="$CXXFLAGS"
pushd build/linux-x86_64-normal-server-release/
make all WARNINGS_ARE_ERRORS= 
make install
popd

# Remove all the binaries installed in /usr/lib/bin. All of them are 
# symlinks and will be created later
rm -rf %{buildroot}/usr/lib/bin

# Change the directory name
pushd %{buildroot}/usr/lib/jvm
mv openjdk-1.8.0-internal java-1.8.0-openjdk
popd

# Remove the copied keystore and link it to the runtime store
rm -f %{buildroot}/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/security/cacerts
ln -s /var/cache/ca-certs/compat/ca-roots.keystore %{buildroot}/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/security/cacerts

mkdir -p %{buildroot}/usr/lib64
ln -s /usr/lib/jvm/java-1.8.0-openjdk/lib/amd64/jli/libjli.so %{buildroot}/usr/lib64/libjli.so

mkdir -p %{buildroot}/usr/bin
# Basic binaries
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/java %{buildroot}/usr/bin/java
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/jjs %{buildroot}/usr/bin/jjs
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/keytool %{buildroot}/usr/bin/keytool
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/orbd %{buildroot}/usr/bin/orbd
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/pack200 %{buildroot}/usr/bin/pack200
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/policytool %{buildroot}/usr/bin/policytool
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/rmid %{buildroot}/usr/bin/rmid
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/rmiregistry %{buildroot}/usr/bin/rmiregistry
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/servertool %{buildroot}/usr/bin/servertool
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/tnameserv %{buildroot}/usr/bin/tnameserv
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/unpack200 %{buildroot}/usr/bin/unpack200

# Dev binaries
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/appletviewer %{buildroot}/usr/bin/appletviewer
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/extcheck %{buildroot}/usr/bin/extcheck
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/idlj %{buildroot}/usr/bin/idlj
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/jar %{buildroot}/usr/bin/jar
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/jarsigner %{buildroot}/usr/bin/jarsigner
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/java-rmi.cgi %{buildroot}/usr/bin/java-rmi.cgi
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/javac %{buildroot}/usr/bin/javac
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/javadoc %{buildroot}/usr/bin/javadoc
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/javah %{buildroot}/usr/bin/javah
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/javap %{buildroot}/usr/bin/javap
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/jcmd %{buildroot}/usr/bin/jcmd
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/jconsole %{buildroot}/usr/bin/jconsole
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/jdb %{buildroot}/usr/bin/jdb
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/jdeps %{buildroot}/usr/bin/jdeps
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/jhat %{buildroot}/usr/bin/jhat
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/jinfo %{buildroot}/usr/bin/jinfo
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/jmap %{buildroot}/usr/bin/jmap
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/jps %{buildroot}/usr/bin/jps
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/jrunscript %{buildroot}/usr/bin/jrunscript
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/jsadebugd %{buildroot}/usr/bin/jsadebugd
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/jstack %{buildroot}/usr/bin/jstack
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/jstat %{buildroot}/usr/bin/jstat
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/jstatd %{buildroot}/usr/bin/jstatd
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/native2ascii %{buildroot}/usr/bin/native2ascii
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/rmic %{buildroot}/usr/bin/rmic
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/schemagen %{buildroot}/usr/bin/schemagen
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/serialver %{buildroot}/usr/bin/serialver
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/wsgen %{buildroot}/usr/bin/wsgen
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/wsimport %{buildroot}/usr/bin/wsimport
ln -s /usr/lib/jvm/java-1.8.0-openjdk/bin/xjc %{buildroot}/usr/bin/xjc

%files
%defattr(-,root,root,-)
/usr/lib/jvm/java-1.8.0-openjdk/ASSEMBLY_EXCEPTION
/usr/lib/jvm/java-1.8.0-openjdk/LICENSE
/usr/lib/jvm/java-1.8.0-openjdk/THIRD_PARTY_README
/usr/lib/jvm/java-1.8.0-openjdk/demo/README
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/ArcTest/ArcCanvas.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/ArcTest/ArcControls.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/ArcTest/ArcTest.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/ArcTest/ArcTest.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/ArcTest/IntegerTextField.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/ArcTest/example1.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/BarChart/BarChart.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/BarChart/BarChart.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/BarChart/example1.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/BarChart/example2.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/Blink/Blink$1.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/Blink/Blink.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/Blink/Blink.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/Blink/example1.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/CardTest/CardPanel.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/CardTest/CardTest.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/CardTest/CardTest.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/CardTest/example1.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/Clock/Clock.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/Clock/Clock.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/Clock/example1.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/DitherTest/CardinalTextField.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/DitherTest/DitherCanvas.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/DitherTest/DitherControls.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/DitherTest/DitherMethod.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/DitherTest/DitherTest$1.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/DitherTest/DitherTest.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/DitherTest/DitherTest.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/DitherTest/example1.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/DrawTest/DrawControls.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/DrawTest/DrawPanel.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/DrawTest/DrawTest.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/DrawTest/DrawTest.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/DrawTest/example1.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/Fractal/CLSFractal.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/Fractal/CLSFractal.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/Fractal/CLSRule.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/Fractal/CLSTurtle.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/Fractal/ContextLSystem.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/Fractal/example1.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/GraphicsTest/AppletFrame.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/GraphicsTest/AppletFrame.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/GraphicsTest/ArcCard.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/GraphicsTest/ArcDegreePanel.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/GraphicsTest/ArcPanel.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/GraphicsTest/ColorUtils.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/GraphicsTest/GraphicsCards.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/GraphicsTest/GraphicsPanel.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/GraphicsTest/GraphicsTest.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/GraphicsTest/GraphicsTest.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/GraphicsTest/OvalShape.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/GraphicsTest/PolygonShape.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/GraphicsTest/RectShape.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/GraphicsTest/RoundRectShape.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/GraphicsTest/Shape.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/GraphicsTest/ShapeTest.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/GraphicsTest/example1.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/MoleculeViewer/Matrix3D.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/MoleculeViewer/MoleculeViewer.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/MoleculeViewer/XYZApp.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/MoleculeViewer/example1.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/MoleculeViewer/example2.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/MoleculeViewer/example3.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/MoleculeViewer/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/NervousText/NervousText.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/NervousText/NervousText.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/NervousText/example1.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SimpleGraph/GraphApplet.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SimpleGraph/GraphApplet.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SimpleGraph/example1.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SortDemo/BidirBubbleSortAlgorithm.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SortDemo/BidirBubbleSortAlgorithm.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SortDemo/BubbleSortAlgorithm.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SortDemo/BubbleSortAlgorithm.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SortDemo/QSortAlgorithm.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SortDemo/QSortAlgorithm.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SortDemo/SortAlgorithm.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SortDemo/SortAlgorithm.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SortDemo/SortItem.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SortDemo/SortItem.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SortDemo/example1.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SpreadSheet/Cell.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SpreadSheet/CellUpdater.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SpreadSheet/InputField.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SpreadSheet/Node.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SpreadSheet/SpreadSheet.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SpreadSheet/SpreadSheet.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SpreadSheet/SpreadSheetInput.class
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/SpreadSheet/example1.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/WireFrame/Matrix3D.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/WireFrame/ThreeD.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/WireFrame/WireFrame.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/WireFrame/example1.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/WireFrame/example2.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/WireFrame/example3.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/WireFrame/example4.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/applets/WireFrame/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/CodePointIM/CodePointIM.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/CodePointIM/README.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/CodePointIM/README_ja.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/CodePointIM/README_zh_CN.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/CodePointIM/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/FileChooserDemo/FileChooserDemo.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/FileChooserDemo/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/FileChooserDemo/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/Font2DTest/Font2DTest.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/Font2DTest/Font2DTest.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/Font2DTest/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/Font2DTest/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/Metalworks/Metalworks.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/Metalworks/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/Metalworks/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/Notepad/Notepad.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/Notepad/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/Notepad/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/SampleTree/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/SampleTree/SampleTree.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/SampleTree/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/SwingApplet/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/SwingApplet/SwingApplet.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/SwingApplet/SwingApplet.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/SwingApplet/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/TableExample/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/TableExample/TableExample.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/TableExample/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/TransparentRuler/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/TransparentRuler/TransparentRuler.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/jfc/TransparentRuler/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/jpda/com/sun/tools/example/README
/usr/lib/jvm/java-1.8.0-openjdk/demo/jpda/examples.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/jpda/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/compiledMethodLoad/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/compiledMethodLoad/lib/libcompiledMethodLoad.so
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/compiledMethodLoad/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/gctest/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/gctest/lib/libgctest.so
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/gctest/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/heapTracker/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/heapTracker/heapTracker.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/heapTracker/lib/libheapTracker.so
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/heapTracker/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/heapViewer/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/heapViewer/lib/libheapViewer.so
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/heapViewer/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/hprof/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/hprof/lib/libhprof.so
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/hprof/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/index.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/minst/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/minst/lib/libminst.so
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/minst/minst.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/minst/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/mtrace/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/mtrace/lib/libmtrace.so
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/mtrace/mtrace.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/mtrace/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/versionCheck/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/versionCheck/lib/libversionCheck.so
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/versionCheck/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/waiters/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/waiters/lib/libwaiters.so
/usr/lib/jvm/java-1.8.0-openjdk/demo/jvmti/waiters/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/management/FullThreadDump/FullThreadDump.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/management/FullThreadDump/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/management/FullThreadDump/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/management/JTop/JTop.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/management/JTop/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/management/JTop/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/management/MemoryMonitor/MemoryMonitor.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/management/MemoryMonitor/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/management/MemoryMonitor/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/management/VerboseGC/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/management/VerboseGC/VerboseGC.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/management/VerboseGC/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/management/index.html
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/FileChooserDemo/build.properties
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/FileChooserDemo/build.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/FileChooserDemo/nbproject/file-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/FileChooserDemo/nbproject/jdk.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/FileChooserDemo/nbproject/netbeans-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/FileChooserDemo/nbproject/project.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/Font2DTest/build.properties
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/Font2DTest/build.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/Font2DTest/nbproject/file-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/Font2DTest/nbproject/jdk.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/Font2DTest/nbproject/netbeans-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/Font2DTest/nbproject/project.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/Metalworks/build.properties
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/Metalworks/build.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/Metalworks/nbproject/file-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/Metalworks/nbproject/jdk.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/Metalworks/nbproject/netbeans-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/Metalworks/nbproject/project.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/Notepad/build.properties
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/Notepad/build.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/Notepad/nbproject/file-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/Notepad/nbproject/jdk.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/Notepad/nbproject/netbeans-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/Notepad/nbproject/project.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/SampleTree/build.properties
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/SampleTree/build.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/SampleTree/nbproject/file-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/SampleTree/nbproject/jdk.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/SampleTree/nbproject/netbeans-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/SampleTree/nbproject/project.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/SwingApplet/build.properties
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/SwingApplet/build.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/SwingApplet/nbproject/file-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/SwingApplet/nbproject/jdk.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/SwingApplet/nbproject/netbeans-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/SwingApplet/nbproject/project.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/TableExample/build.properties
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/TableExample/build.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/TableExample/nbproject/file-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/TableExample/nbproject/jdk.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/TableExample/nbproject/netbeans-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/TableExample/nbproject/project.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/TransparentRuler/build.properties
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/TransparentRuler/build.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/TransparentRuler/nbproject/file-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/TransparentRuler/nbproject/jdk.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/TransparentRuler/nbproject/netbeans-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/jfc/TransparentRuler/nbproject/project.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/FullThreadDump/build.properties
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/FullThreadDump/build.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/FullThreadDump/nbproject/file-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/FullThreadDump/nbproject/jdk.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/FullThreadDump/nbproject/netbeans-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/FullThreadDump/nbproject/project.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/JTop/build.properties
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/JTop/build.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/JTop/nbproject/file-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/JTop/nbproject/jdk.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/JTop/nbproject/netbeans-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/JTop/nbproject/project.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/MemoryMonitor/build.properties
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/MemoryMonitor/build.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/MemoryMonitor/nbproject/file-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/MemoryMonitor/nbproject/jdk.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/MemoryMonitor/nbproject/netbeans-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/MemoryMonitor/nbproject/project.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/VerboseGC/build.properties
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/VerboseGC/build.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/VerboseGC/nbproject/file-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/VerboseGC/nbproject/jdk.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/VerboseGC/nbproject/netbeans-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/management/VerboseGC/nbproject/project.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/project.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/scripting/jconsole-plugin/build.properties
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/scripting/jconsole-plugin/build.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/scripting/jconsole-plugin/nbproject/file-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/scripting/jconsole-plugin/nbproject/jdk.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/scripting/jconsole-plugin/nbproject/netbeans-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nbproject/scripting/jconsole-plugin/nbproject/project.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/nio/zipfs/Demo.java
/usr/lib/jvm/java-1.8.0-openjdk/demo/nio/zipfs/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/nio/zipfs/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/demo/nio/zipfs/zipfs.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/scripting/jconsole-plugin/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/demo/scripting/jconsole-plugin/build.xml
/usr/lib/jvm/java-1.8.0-openjdk/demo/scripting/jconsole-plugin/jconsole-plugin.jar
/usr/lib/jvm/java-1.8.0-openjdk/demo/scripting/jconsole-plugin/src.zip
/usr/lib/jvm/java-1.8.0-openjdk/jre/ASSEMBLY_EXCEPTION
/usr/lib/jvm/java-1.8.0-openjdk/jre/LICENSE
/usr/lib/jvm/java-1.8.0-openjdk/jre/THIRD_PARTY_README
/usr/lib/jvm/java-1.8.0-openjdk/jre/bin/java
/usr/lib/jvm/java-1.8.0-openjdk/jre/bin/jjs
/usr/lib/jvm/java-1.8.0-openjdk/jre/bin/keytool
/usr/lib/jvm/java-1.8.0-openjdk/jre/bin/orbd
/usr/lib/jvm/java-1.8.0-openjdk/jre/bin/pack200
/usr/lib/jvm/java-1.8.0-openjdk/jre/bin/policytool
/usr/lib/jvm/java-1.8.0-openjdk/jre/bin/rmid
/usr/lib/jvm/java-1.8.0-openjdk/jre/bin/rmiregistry
/usr/lib/jvm/java-1.8.0-openjdk/jre/bin/servertool
/usr/lib/jvm/java-1.8.0-openjdk/jre/bin/tnameserv
/usr/lib/jvm/java-1.8.0-openjdk/jre/bin/unpack200
/usr/lib/jvm/java-1.8.0-openjdk/release
/usr/lib/jvm/java-1.8.0-openjdk/sample/README
/usr/lib/jvm/java-1.8.0-openjdk/sample/annotations/DependencyChecker/PluginChecker/src/checker/Device.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/annotations/DependencyChecker/PluginChecker/src/checker/Kettle.xml
/usr/lib/jvm/java-1.8.0-openjdk/sample/annotations/DependencyChecker/PluginChecker/src/checker/Module.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/annotations/DependencyChecker/PluginChecker/src/checker/PluginChecker.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/annotations/DependencyChecker/PluginChecker/src/checker/Require.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/annotations/DependencyChecker/PluginChecker/src/checker/RequireContainer.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/annotations/DependencyChecker/Plugins/src/plugins/BoilerPlugin.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/annotations/DependencyChecker/Plugins/src/plugins/ExtendedBoilerPlugin.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/annotations/DependencyChecker/Plugins/src/plugins/TimerPlugin.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/annotations/Validator/src/PositiveIntegerSupplier.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/annotations/Validator/src/SupplierValidator.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/annotations/Validator/src/Validate.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/annotations/Validator/src/Validator.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/annotations/index.html
/usr/lib/jvm/java-1.8.0-openjdk/sample/forkjoin/mergesort/MergeDemo.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/forkjoin/mergesort/MergeSort.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/build.properties
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/build.xml
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/docfiles/connect-local-ant-run.jpg
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/docfiles/connect-local-java-jar.jpg
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/docfiles/connect-local.jpg
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/docfiles/remote-connection-failed.jpg
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/docfiles/remote-connection.jpg
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/docfiles/scandir-config.jpg
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/docfiles/scandir-result.jpg
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/docfiles/scandir-start.jpg
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/index.html
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/keystore
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/logging.properties
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/manifest.mf
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/nbproject/file-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/nbproject/jdk.xml
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/nbproject/netbeans-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/nbproject/project.xml
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/DirectoryScanner.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/DirectoryScannerMXBean.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/ResultLogManager.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/ResultLogManagerMXBean.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/ScanDirAgent.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/ScanDirClient.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/ScanDirConfig.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/ScanDirConfigMXBean.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/ScanManager.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/ScanManagerMXBean.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/config/DirectoryScannerConfig.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/config/FileMatch.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/config/ResultLogConfig.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/config/ResultRecord.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/config/ScanManagerConfig.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/config/XmlConfigUtils.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/config/package.html
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/package.html
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/etc/access.properties
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/etc/management.properties
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/etc/password.properties
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/src/etc/testconfig.xml
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/test/com/sun/jmx/examples/scandir/DirectoryScannerTest.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/test/com/sun/jmx/examples/scandir/ScanDirConfigTest.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/test/com/sun/jmx/examples/scandir/ScanManagerTest.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/test/com/sun/jmx/examples/scandir/TestUtils.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/test/com/sun/jmx/examples/scandir/config/XmlConfigUtilsTest.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/jmx/jmx-scandir/truststore
/usr/lib/jvm/java-1.8.0-openjdk/sample/lambda/BulkDataOperations/index.html
/usr/lib/jvm/java-1.8.0-openjdk/sample/lambda/BulkDataOperations/src/CSVProcessor.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/lambda/BulkDataOperations/src/Grep.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/lambda/BulkDataOperations/src/PasswordGenerator.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/lambda/BulkDataOperations/src/WC.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/lambda/DefaultMethods/ArrayIterator.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/lambda/DefaultMethods/DiamondInheritance.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/lambda/DefaultMethods/Inheritance.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/lambda/DefaultMethods/MixIn.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/lambda/DefaultMethods/Reflection.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/lambda/DefaultMethods/SimplestUsage.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nbproject/project.xml
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/chatserver/ChatServer.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/chatserver/Client.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/chatserver/ClientReader.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/chatserver/DataReader.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/chatserver/MessageReader.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/chatserver/NameReader.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/chatserver/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/file/AclEdit.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/file/Chmod.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/file/Copy.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/file/DiskUsage.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/file/FileType.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/file/WatchDir.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/file/Xdd.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/multicast/MulticastAddress.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/multicast/Reader.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/multicast/Sender.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/AcceptHandler.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/Acceptor.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/B1.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/BN.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/BP.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/ChannelIO.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/ChannelIOSecure.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/Content.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/Dispatcher.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/Dispatcher1.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/DispatcherN.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/FileContent.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/Handler.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/MalformedRequestException.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/N1.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/N2.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/Reply.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/Request.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/RequestHandler.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/RequestServicer.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/Sendable.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/Server.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/StringContent.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/nio/server/URLDumper.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/build.properties
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/build.xml
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/nbproject/file-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/nbproject/jdk.xml
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/nbproject/netbeans-targets.xml
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/nbproject/project.xml
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/src/META-INF/manifest.mf
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/src/com/sun/sample/scriptpad/Main.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/src/resources/Main.js
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/src/resources/conc.js
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/src/resources/gui.js
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/src/resources/mm.js
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/src/resources/scriptpad.js
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/src/scripts/README.txt
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/src/scripts/browse.js
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/src/scripts/insertfile.js
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/src/scripts/linewrap.js
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/src/scripts/mail.js
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/src/scripts/memmonitor.js
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/src/scripts/memory.bat
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/src/scripts/memory.js
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/src/scripts/memory.sh
/usr/lib/jvm/java-1.8.0-openjdk/sample/scripting/scriptpad/src/scripts/textcolor.js
/usr/lib/jvm/java-1.8.0-openjdk/sample/try-with-resources/index.html
/usr/lib/jvm/java-1.8.0-openjdk/sample/try-with-resources/src/CustomAutoCloseableSample.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/try-with-resources/src/Unzip.java
/usr/lib/jvm/java-1.8.0-openjdk/sample/try-with-resources/src/ZipCat.java
/usr/lib/jvm/java-1.8.0-openjdk/src.zip

%files bin
/usr/bin/java
/usr/bin/jjs
/usr/bin/keytool
/usr/bin/orbd
/usr/bin/pack200
/usr/bin/policytool
/usr/bin/rmid
/usr/bin/rmiregistry
/usr/bin/servertool
/usr/bin/tnameserv
/usr/bin/unpack200
/usr/lib/jvm/java-1.8.0-openjdk/bin/java
/usr/lib/jvm/java-1.8.0-openjdk/bin/jjs
/usr/lib/jvm/java-1.8.0-openjdk/bin/keytool
/usr/lib/jvm/java-1.8.0-openjdk/bin/orbd
/usr/lib/jvm/java-1.8.0-openjdk/bin/pack200
/usr/lib/jvm/java-1.8.0-openjdk/bin/policytool
/usr/lib/jvm/java-1.8.0-openjdk/bin/rmid
/usr/lib/jvm/java-1.8.0-openjdk/bin/rmiregistry
/usr/lib/jvm/java-1.8.0-openjdk/bin/servertool
/usr/lib/jvm/java-1.8.0-openjdk/bin/tnameserv
/usr/lib/jvm/java-1.8.0-openjdk/bin/unpack200

%files lib
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/jli/libjli.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/jli/libjli.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/jvm.cfg
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libattach.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libattach.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libawt.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libawt.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libawt_headless.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libawt_headless.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libawt_xawt.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libawt_xawt.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libdt_socket.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libdt_socket.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libfontmanager.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libfontmanager.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libhprof.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libhprof.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libinstrument.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libinstrument.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libj2gss.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libj2gss.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libj2pcsc.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libj2pcsc.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libj2pkcs11.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libj2pkcs11.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjaas_unix.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjaas_unix.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjava.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjava.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjava_crw_demo.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjava_crw_demo.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjawt.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjawt.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjdwp.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjdwp.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjpeg.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjpeg.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjsdt.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjsdt.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjsig.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjsig.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjsound.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjsound.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjsoundalsa.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libjsoundalsa.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/liblcms.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/liblcms.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libmanagement.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libmanagement.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libmlib_image.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libmlib_image.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libnet.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libnet.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libnio.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libnio.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libnpt.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libnpt.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libsaproc.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libsaproc.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libsctp.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libsctp.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libsplashscreen.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libsplashscreen.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libsunec.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libsunec.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libunpack.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libunpack.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libverify.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libverify.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libzip.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/libzip.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/server/Xusage.txt
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/server/libjsig.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/server/libjsig.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/server/libjvm.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/amd64/server/libjvm.so
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/calendars.properties
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/charsets.jar
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/classlist
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/cmm/CIEXYZ.pf
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/cmm/GRAY.pf
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/cmm/LINEAR_RGB.pf
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/cmm/PYCC.pf
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/cmm/sRGB.pf
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/content-types.properties
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/currency.data
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/ext/cldrdata.jar
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/ext/dnsns.jar
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/ext/jaccess.jar
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/ext/localedata.jar
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/ext/meta-index
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/ext/nashorn.jar
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/ext/sunec.jar
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/ext/sunjce_provider.jar
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/ext/sunpkcs11.jar
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/ext/zipfs.jar
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/flavormap.properties
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/hijrah-config-umalqura.properties
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/images/cursors/cursors.properties
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/images/cursors/invalid32x32.gif
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/images/cursors/motif_CopyDrop32x32.gif
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/images/cursors/motif_CopyNoDrop32x32.gif
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/images/cursors/motif_LinkDrop32x32.gif
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/images/cursors/motif_LinkNoDrop32x32.gif
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/images/cursors/motif_MoveDrop32x32.gif
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/images/cursors/motif_MoveNoDrop32x32.gif
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/jce.jar
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/jexec
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/jexec.diz
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/jsse.jar
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/jvm.hprof.txt
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/logging.properties
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/management-agent.jar
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/management/jmxremote.access
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/management/jmxremote.password.template
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/management/management.properties
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/management/snmp.acl.template
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/meta-index
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/net.properties
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/psfont.properties.ja
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/psfontj2d.properties
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/resources.jar
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/rt.jar
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/security/blacklisted.certs
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/security/cacerts
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/security/java.policy
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/security/java.security
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/security/policy/limited/US_export_policy.jar
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/security/policy/limited/local_policy.jar
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/security/policy/unlimited/US_export_policy.jar
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/security/policy/unlimited/local_policy.jar
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/sound.properties
/usr/lib/jvm/java-1.8.0-openjdk/jre/lib/tzdb.dat
/usr/lib/jvm/java-1.8.0-openjdk/lib/amd64/jli/libjli.so
/usr/lib/jvm/java-1.8.0-openjdk/lib/amd64/libjawt.so
/usr/lib/jvm/java-1.8.0-openjdk/lib/ct.sym
/usr/lib/jvm/java-1.8.0-openjdk/lib/dt.jar
/usr/lib/jvm/java-1.8.0-openjdk/lib/ir.idl
/usr/lib/jvm/java-1.8.0-openjdk/lib/jconsole.jar
/usr/lib/jvm/java-1.8.0-openjdk/lib/jexec
/usr/lib/jvm/java-1.8.0-openjdk/lib/orb.idl
/usr/lib/jvm/java-1.8.0-openjdk/lib/sa-jdi.jar
/usr/lib/jvm/java-1.8.0-openjdk/lib/tools.jar
/usr/lib64/libjli.so

%files dev
/usr/bin/appletviewer
/usr/bin/extcheck
/usr/bin/idlj
/usr/bin/jar
/usr/bin/jarsigner
/usr/bin/java-rmi.cgi
/usr/bin/javac
/usr/bin/javadoc
/usr/bin/javah
/usr/bin/javap
/usr/bin/jcmd
/usr/bin/jconsole
/usr/bin/jdb
/usr/bin/jdeps
/usr/bin/jhat
/usr/bin/jinfo
/usr/bin/jmap
/usr/bin/jps
/usr/bin/jrunscript
/usr/bin/jsadebugd
/usr/bin/jstack
/usr/bin/jstat
/usr/bin/jstatd
/usr/bin/native2ascii
/usr/bin/rmic
/usr/bin/schemagen
/usr/bin/serialver
/usr/bin/wsgen
/usr/bin/wsimport
/usr/bin/xjc
/usr/lib/jvm/java-1.8.0-openjdk/bin/appletviewer
/usr/lib/jvm/java-1.8.0-openjdk/bin/extcheck
/usr/lib/jvm/java-1.8.0-openjdk/bin/idlj
/usr/lib/jvm/java-1.8.0-openjdk/bin/jar
/usr/lib/jvm/java-1.8.0-openjdk/bin/jarsigner
/usr/lib/jvm/java-1.8.0-openjdk/bin/java-rmi.cgi
/usr/lib/jvm/java-1.8.0-openjdk/bin/javac
/usr/lib/jvm/java-1.8.0-openjdk/bin/javadoc
/usr/lib/jvm/java-1.8.0-openjdk/bin/javah
/usr/lib/jvm/java-1.8.0-openjdk/bin/javap
/usr/lib/jvm/java-1.8.0-openjdk/bin/jcmd
/usr/lib/jvm/java-1.8.0-openjdk/bin/jconsole
/usr/lib/jvm/java-1.8.0-openjdk/bin/jdb
/usr/lib/jvm/java-1.8.0-openjdk/bin/jdeps
/usr/lib/jvm/java-1.8.0-openjdk/bin/jhat
/usr/lib/jvm/java-1.8.0-openjdk/bin/jinfo
/usr/lib/jvm/java-1.8.0-openjdk/bin/jmap
/usr/lib/jvm/java-1.8.0-openjdk/bin/jps
/usr/lib/jvm/java-1.8.0-openjdk/bin/jrunscript
/usr/lib/jvm/java-1.8.0-openjdk/bin/jsadebugd
/usr/lib/jvm/java-1.8.0-openjdk/bin/jstack
/usr/lib/jvm/java-1.8.0-openjdk/bin/jstat
/usr/lib/jvm/java-1.8.0-openjdk/bin/jstatd
/usr/lib/jvm/java-1.8.0-openjdk/bin/native2ascii
/usr/lib/jvm/java-1.8.0-openjdk/bin/rmic
/usr/lib/jvm/java-1.8.0-openjdk/bin/schemagen
/usr/lib/jvm/java-1.8.0-openjdk/bin/serialver
/usr/lib/jvm/java-1.8.0-openjdk/bin/wsgen
/usr/lib/jvm/java-1.8.0-openjdk/bin/wsimport
/usr/lib/jvm/java-1.8.0-openjdk/bin/xjc
/usr/lib/jvm/java-1.8.0-openjdk/include/classfile_constants.h
/usr/lib/jvm/java-1.8.0-openjdk/include/jawt.h
/usr/lib/jvm/java-1.8.0-openjdk/include/jdwpTransport.h
/usr/lib/jvm/java-1.8.0-openjdk/include/jni.h
/usr/lib/jvm/java-1.8.0-openjdk/include/jvmti.h
/usr/lib/jvm/java-1.8.0-openjdk/include/jvmticmlr.h
/usr/lib/jvm/java-1.8.0-openjdk/include/linux/jawt_md.h
/usr/lib/jvm/java-1.8.0-openjdk/include/linux/jni_md.h

%files doc
/usr/lib/jvm/java-1.8.0-openjdk/man/ja
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/appletviewer.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/extcheck.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/idlj.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/jar.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/jarsigner.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/java.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/javac.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/javadoc.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/javah.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/javap.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/jcmd.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/jconsole.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/jdb.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/jdeps.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/jhat.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/jinfo.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/jjs.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/jmap.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/jps.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/jrunscript.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/jsadebugd.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/jstack.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/jstat.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/jstatd.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/keytool.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/native2ascii.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/orbd.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/pack200.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/policytool.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/rmic.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/rmid.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/rmiregistry.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/schemagen.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/serialver.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/servertool.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/tnameserv.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/unpack200.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/wsgen.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/wsimport.1
/usr/lib/jvm/java-1.8.0-openjdk/man/ja_JP.UTF-8/man1/xjc.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/appletviewer.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/extcheck.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/idlj.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/jar.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/jarsigner.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/java.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/javac.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/javadoc.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/javah.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/javap.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/jcmd.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/jconsole.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/jdb.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/jdeps.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/jhat.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/jinfo.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/jjs.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/jmap.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/jps.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/jrunscript.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/jsadebugd.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/jstack.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/jstat.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/jstatd.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/keytool.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/native2ascii.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/orbd.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/pack200.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/policytool.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/rmic.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/rmid.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/rmiregistry.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/schemagen.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/serialver.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/servertool.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/tnameserv.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/unpack200.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/wsgen.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/wsimport.1
/usr/lib/jvm/java-1.8.0-openjdk/man/man1/xjc.1

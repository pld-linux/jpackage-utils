%define 	jpackage_distver 1.7
Summary:	JPackage utilities
Summary(pl.UTF-8):	Narzędzia JPackage
Name:		jpackage-utils
Version:	1.7.5
Release:	1
Epoch:		0
License:	BSD-like
Group:		Development/Languages/Java
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	5039b51d1e80e45da27faf131448eaa8
Patch0:		%{name}-pdksh.patch
Patch1:		%{name}-checkdir.patch
Patch2:		%{name}-errors.patch
Patch3:		%{name}-noyelling.patch
Patch4:		%{name}-readlink.patch
URL:		http://www.jpackage.org/
BuildRequires:	rpmbuild(macros) >= 1.409
Requires:	/bin/egrep
Requires:	/bin/sed
Requires:	which
Conflicts:	rpmbuild(macros) < 1.409
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utilities from the JPackage Project <http://www.jpackage.org/>:

- build-classpath - build the Java classpath in a portable manner
- build-jar-repository - build a jar repository in a portable manner
- rebuild-jar-repository - rebuild a jar repository in a portable
  manner (after a jvm change...)
- build-classpath-directory - build the Java classpath from a
  directory
- diff-jars - show jar content differences
- jvmjar - install jvm extensions
- create-jar-links - create custom jar links
- clean-binary-files - remove binary files from sources
- check-binary-files - check for presence of unexpected binary files
- %{_datadir}/java-utils/java-functions - shell script functions
  library for Java applications
- %{_sysconfdir}/java/jpackage-release - string identifying the
  currently installed JPackage release
- %{_sysconfdir}/java/java.conf - system-wide Java configuration file
- %{_docdir}/%{name}-%{version}/jpackage-policy - Java packaging
  policy for packagers and developers of JPackage Project

It contains also the License, man pages, documentation, XSL files of
general use with maven2, a header file for spec files etc.

%description -l pl.UTF-8
Narzędzia z projektu JPackage <http://www.jpackage.org/>:

- build-classpath tworzy ścieżkę do klas (classpath) Javy w sposób
  przenośny
- build-jar-repository tworzy repozytorium jar w sposób przenośny
- rebuild-jar-repository przebudowuje repozytorium jar w przenośny
  sposób (po zmianie jvm)
- build-classpath-directory tworzy ścieżkę do klas (classpath) Javy
  z katalogu
- diff-jars pokazuje różnice między zawartością jarów
- jvmjar instaluje rozszerzenia jvm
- create-jar-links tworzy własne dowiązania do jarów
- clean-binary-files usuwa binarne pliki ze źródeł
- check-binary-files sprawdza istnienie nieoczekiwanych plików
  binarnych
- %{_datadir}/java-utils/java-functions to biblioteka funkcji
  skryptów powłoki dla aplikacji w Javie
- %{_sysconfdir}/java/jpackage-release to łańcuch określający
  aktualnie zainstalowane wydanie JPackage
- %{_sysconfdir}/java/java.conf to ogólnosystemowy plik
  konfiguracyjny Javy
- %{_docdir}/%{name}-%{version}/jpackage-policy to polityka
  pakietowania Javy dla osób pakietujących i programistów z projektu
  JPackage

Pakiet zawiera także treść licencji, strony manuala, dokumentację,
pliki XSL dla programu maven2, plik nagłówkowy dla plików spec itp.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# we cp -a complete dir from source
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
echo "JPackage release %{jpackage_distver} (PLD Linux port) for %{_build_arch}" > etc/jpackage-release

%install
rm -rf $RPM_BUILD_ROOT

# arch independant
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/java,/etc/env.d,%{_javadocdir},%{_javadir}} \
	$RPM_BUILD_ROOT{%{_jvmsysconfdir},%{_jvmcommondatadir},%{_jvmdatadir},%{_jvmcommonsysconfdir}} \
	$RPM_BUILD_ROOT%{_javadir}-{utils,ext,1.4.0,1.4.1,1.4.2,1.5.0,1.6.0} \
	$RPM_BUILD_ROOT%{_mavendepmapdir}

# arch dependant
install -d \
	$RPM_BUILD_ROOT{%{_jvmdir},%{_jvmjardir},%{_jvmprivdir},%{_jvmcommonlibdir},%{_jnidir}} \
	$RPM_BUILD_ROOT%{_jnidir}-{ext,1.4.0,1.4.1,1.4.2,1.5.0,1.6.0}

%if "%{_lib}" != "lib"
%define _ujvmdir			%{_prefix}/lib/jvm
%define _ujvmjardir			%{_prefix}/lib/jvm-exports
%define _ujvmprivdir		%{_prefix}/lib/jvm-private
%define _ujvmcommonlibdir	%{_prefix}/lib/jvm-common
%define _ujnidir			%{_prefix}/lib/java
%define _ujvmlibdir			%{_prefix}/lib/jvm

install -d \
	$RPM_BUILD_ROOT{%{_ujvmdir},%{_ujvmjardir},%{_ujvmprivdir},%{_ujvmcommonlibdir},%{_ujnidir}} \
	$RPM_BUILD_ROOT%{_ujnidir}-{ext,1.4.0,1.4.1,1.4.2,1.5.0,1.6.0}
%endif

install -pm 755 bin/* $RPM_BUILD_ROOT%{_bindir}
install -pm 644 etc/font.properties $RPM_BUILD_ROOT%{_sysconfdir}/java

# Create an initial (empty) depmap
echo -e "<dependencies>\\n" > ${RPM_BUILD_ROOT}%{_mavendepmapdir}/maven2-depmap.xml
echo -e "</dependencies>\\n" >> ${RPM_BUILD_ROOT}%{_mavendepmapdir}/maven2-depmap.xml

cat > etc/java.conf << 'EOF'
# System-wide Java configuration file                                -*- sh -*-
#
# JPackage Project <http://www.jpackage.org/>

# Location of jar files on the system
JAVA_LIBDIR=%{_javadir}

# Location of arch-specific jar files on the system
JNI_LIBDIR=%{_jnidir}

# Root of all JVM installations
JVM_ROOT=%{_jvmdir}

# You can define a system-wide JVM root here if you're not using the default one
#JAVA_HOME=$JVM_ROOT/java

# Options to pass to the java interpreter
JAVACMD_OPTS=
EOF

install -pm 644 etc/java.conf $RPM_BUILD_ROOT%{_sysconfdir}/java
install -pm 644 etc/jpackage-release $RPM_BUILD_ROOT%{_sysconfdir}/java
install -pm 644 java-utils/* $RPM_BUILD_ROOT%{_javadir}-utils
install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp -a man/* $RPM_BUILD_ROOT%{_mandir}/man1
install -d $RPM_BUILD_ROOT%{_javadir}-utils/xml
cp -a xml/* $RPM_BUILD_ROOT%{_javadir}-utils/xml

cat << 'EOF' >$RPM_BUILD_ROOT/etc/env.d/JAVA_HOME
JAVA_HOME=$(. %{_javadir}-utils/java-functions; set_jvm >&2; echo "$JAVA_HOME")
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%env_update

%postun
%env_update

%files
%defattr(644,root,root,755)
%doc LICENSE.txt doc/* etc/httpd-javadoc.conf
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}/java
%config %{_sysconfdir}/java/jpackage-release
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/java/java.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/java/font.properties
%config(noreplace,missingok) %verify(not md5 mtime size) /etc/env.d/*
%{_mandir}/man1/*
%{_javadir}-utils/*
%dir %{_mavendepmapdir}
%config(noreplace) %verify(not md5 mtime size) %{_mavendepmapdir}/maven2-depmap.xml
%dir %{_javadir}
%dir %{_javadir}-*
%docdir %{_javadocdir}
%dir %{_javadocdir}

# arch dependant
%dir %{_jvmdir}
%dir %{_jvmjardir}
%dir %{_jvmprivdir}
%dir %{_jvmcommonlibdir}
%dir %{_jnidir}
%dir %{_jnidir}-*
%if "%{_lib}" != "lib"
%dir %{_ujvmdir}
%dir %{_ujvmjardir}
%dir %{_ujvmprivdir}
%dir %{_ujvmcommonlibdir}
%dir %{_ujnidir}
%dir %{_ujnidir}-*
%endif

# arch independant
%dir %{_jvmdatadir}
%dir %{_jvmsysconfdir}
%dir %{_jvmcommondatadir}
%dir %{_jvmcommonsysconfdir}

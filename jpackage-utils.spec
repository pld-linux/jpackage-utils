# TODO
# - update build macros so that pack200 is used to repackage jars to remove debug information
#   http://java.sun.com/javase/6/docs/technotes/guides/deployment/deployment-guide/pack200.html
%define 	jpackage_distver 1.6
Summary:	JPackage utilities
Summary(pl):	Narzêdzia JPackage
Name:		jpackage-utils
Version:	1.6.6
Release:	15
Epoch:		0
License:	BSD-like
Group:		Development/Languages/Java
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	85336e72018ecefa2f9999fc4e6f3eb8
Patch0:		%{name}-pdksh.patch
Patch1:		%{name}-checkdir.patch
Patch2:		%{name}-errors.patch
URL:		http://www.jpackage.org/
BuildRequires:	rpmbuild(macros) >= 1.318
Requires:	/bin/egrep
Requires:	/bin/sed
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utilities from the JPackage Project <http://www.jpackage.org/>:

- %{_bindir}/build-classpath build the Java classpath in a portable
  manner
- %{_bindir}/build-jar-repository build a jar repository in a portable
  manner
- %{_bindir}/rebuild-jar-repository rebuild a jar repository in a
  portable manner (after a jvm change...)
- %{_bindir}/build-classpath-directory build the Java classpath from a
  directory
- %{_bindir}/diff-jars show jar content differences
- %{_bindir}/jvmjar install jvm extensions
- %{_datadir}/java-utils/java-functions shell script functions library
  for Java applications
- %{_sysconfdir}/java/jpackage-release string identifying the
  currently installed JPackage release
- %{_sysconfdir}/java/java.conf system-wide Java configuration file
- %{_docdir}/%{name}-%{version}/jpackage-policy Java packaging policy
  for packagers and developers of JPackage Project

%description -l pl
Narzêdzia z projektu JPackage <http://www.jpackage.org/>:

- %{_bindir}/build-classpath tworzy ¶cie¿kê do klas (classpath) Javy w
  przeno¶ny sposób
- %{_bindir}/build-jar-repository tworzy repozytorium jar w przeno¶ny
  sposób
- %{_bindir}/rebuild-jar-repository przebudowuje repozytorium jar w
  przeno¶ny sposób (po zmianie jvm)
- %{_bindir}/build-classpath-directory tworzy ¶cie¿kê do klas
  (classpath) Javy z katalogu
- %{_bindir}/diff-jars pokazuje ró¿nice miêdzy zawarto¶ci± jarów
- %{_bindir}/jvmjar instaluje rozszerzenia jvm
- %{_datadir}/java-utils/java-functions to biblioteka funkcji skryptów
  pow³oki dla aplikacji w Javie
- %{_sysconfdir}/java/jpackage-release to ³añcuch okre¶laj±cy
  aktualnie zainstalowane wydanie JPackage
- %{_sysconfdir}/java/java.conf to ogólnosystemowy plik konfiguracyjny
  Javy
- %{_docdir}/%{name}-%{version}/jpackage-policy to polityka
  pakietowania Javy dla osób pakietuj±cych i programistów z projektu
  JPackage

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

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
%dir %{_javadir}
%dir %{_javadir}-*
%docdir %{_javadocdir}
%dir %{_javadocdir}
%{_javadir}-utils/*


%define 	jpackage_distver 1.6
Summary:	JPackage utilities
Name:		jpackage-utils
Version:	1.6.6
Release:	1
Epoch:		0
License:	BSD-like
URL:		http://www.jpackage.org/
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	85336e72018ecefa2f9999fc4e6f3eb8
Patch0:		%{name}-pdksh.patch
Group:		Development/Languages/Java
BuildArch:	noarch
ExclusiveArch:	i586 i686 pentium3 pentium4 athlon %{x8664} noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Requires:	/bin/egrep
Requires:	/bin/sed

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
- %{_sysconfdir}/rpm/macros.jpackage RPM macros for Java packagers and
  developers
- %{_docdir}/%{name}-%{version}/jpackage-policy Java packaging policy
  for packagers and developers of JPackage Project

%prep
%setup -q
%patch0 -p1

%build
echo "JPackage release %{jpackage_distver} (PLD Linux port) for %{buildarch}" > etc/jpackage-release

%install
rm -rf $RPM_BUILD_ROOT

for dir in \
    jvmdir jvmjardir jvmprivdir \
    jvmlibdir jvmdatadir jvmsysconfdir \
    jvmcommonlibdir jvmcommondatadir jvmcommonsysconfdir \
    javadir jnidir javadocdir ; do
  export _${dir}=$(rpm --eval $(%{__grep} -E "^%_${dir}\b" misc/macros.jpackage | %{__awk} '{ print $2 }'))
done

install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/java,${_jvmdir}} \
	$RPM_BUILD_ROOT{/usr/lib/rpm,${_jvmdir},${_javadocdir}} \
	$RPM_BUILD_ROOT{${_jvmjardir},${_jvmprivdir},${_jvmlibdir},${_jvmdatadir}} \
	$RPM_BUILD_ROOT{${_jvmsysconfdir},${_jvmcommonlibdir},${_jvmcommondatadir}} \
	$RPM_BUILD_ROOT{${_jvmcommonsysconfdir},${_javadir},${_jnidir}} \
	$RPM_BUILD_ROOT${_javadir}-{utils,ext,1.4.0,1.4.1,1.4.2,1.5.0} \
	$RPM_BUILD_ROOT${_jnidir}-{ext,1.4.0,1.4.1,1.4.2,1.5.0} \
	$RPM_BUILD_ROOT${_javadocdir}


install -pm 755 bin/* ${RPM_BUILD_ROOT}%{_bindir}
install -pm 644 etc/font.properties ${RPM_BUILD_ROOT}%{_sysconfdir}/java

cat > etc/java.conf << EOF
# System-wide Java configuration file                                -*- sh -*-
#
# JPackage Project <http://www.jpackage.org/>

# Location of jar files on the system
JAVA_LIBDIR=${_javadir}

# Location of arch-specific jar files on the system
JNI_LIBDIR=${_jnidir}

# Root of all JVM installations
JVM_ROOT=${_jvmdir}

# You can define a system-wide JVM root here if you're not using the default one
#JAVA_HOME=\$JVM_ROOT/java

# Options to pass to the java interpreter
JAVACMD_OPTS=
EOF

install -pm 644 etc/java.conf $RPM_BUILD_ROOT%{_sysconfdir}/java
install -pm 644 etc/jpackage-release $RPM_BUILD_ROOT%{_sysconfdir}/java
install -pm 644 java-utils/* $RPM_BUILD_ROOT${_javadir}-utils
awk 'BEGIN {cont=0}
/^#/ { if (!cont) next }
/^%%/ { if (cont) print; else print "%%define " substr($0,2) }
{cont = $0 ~ /\\$/}
/\\\\$/ { print $0 "\\"; next }
$0 !~ /^%%/ {print}
' misc/macros.jpackage > $RPM_BUILD_ROOT/usr/lib/rpm/macros.java

cat <<EOF > %{name}-%{version}.files
%dir ${_jvmdir}
%dir ${_jvmjardir}
%dir ${_jvmprivdir}
# %dir ${_jvmlibdir}
%dir ${_jvmdatadir}
%dir ${_jvmsysconfdir}
%dir ${_jvmcommonlibdir}
%dir ${_jvmcommondatadir}
%dir ${_jvmcommonsysconfdir}
%dir ${_javadir}
%dir ${_javadir}-*
%dir ${_jnidir}
%dir ${_jnidir}-*
%dir ${_javadocdir}
${_javadir}-utils/*
EOF


%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}.files
%defattr(644,root,root,755)
%doc LICENSE.txt doc/* etc/httpd-javadoc.conf
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}/java
%config %{_sysconfdir}/java/jpackage-release
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/java/java.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/java/font.properties
/usr/lib/rpm/macros.java

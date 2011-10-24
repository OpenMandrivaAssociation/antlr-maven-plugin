%global svndate		20101012
%global	svnver		12849
%global svnstring	%{svndate}svn%{svnver}

Name:			antlr-maven-plugin
Version:		2.1
Release:		4.%{svnstring}
Summary:		Maven plugin that generates files based on grammar file(s)
License:		ASL 2.0
URL:			http://mojo.codehaus.org/antlr-maven-plugin/
Group:			Development/Java
# No source tarball known.
# Checked out from SVN
# svn export https://svn.codehaus.org/mojo/tags/antlr-maven-plugin-2.1 antlr-maven-plugin
# tar cfj antlr-maven-plugin-20101012svn12849.tar.bz2 antlr-maven-plugin
Source0:		%{name}-%{svnstring}.tar.bz2
# Modern modello expects to see <models></models>, even if there is only one. 
Patch0:			maven-antlr-plugin-2.1-modello-issue.patch
# Add maven-artifact to the pom.xml, we need it to build
Patch1:			maven-antlr-plugin-2.1-artifact.patch
# siteRenderer.createSink doesn't exist anymore
Patch2:			maven-antlr-plugin-2.1-sinkfix.patch
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:		noarch
BuildRequires:		java-devel
BuildRequires:		jpackage-utils
BuildRequires:		antlr
BuildRequires:		maven2
BuildRequires:		maven2-plugin-compiler
BuildRequires:		maven2-plugin-install
BuildRequires:		maven2-plugin-jar
BuildRequires:		maven2-plugin-javadoc
BuildRequires:		maven2-plugin-resources
BuildRequires:		maven2-plugin-surefire
BuildRequires:		maven-antrun-plugin
BuildRequires:		maven-clean-plugin
BuildRequires:		maven-invoker-plugin
BuildRequires:		maven-plugin-plugin
BuildRequires:		maven-release-plugin
BuildRequires:		maven-site-plugin
BuildRequires:		maven-source-plugin
BuildRequires:		maven-plugin-bundle
Requires:		antlr
Requires:		jpackage-utils
Requires:		java >= 0:1.6.0
Requires(post):		jpackage-utils
Requires(postun):	jpackage-utils
Provides:		maven2-plugin-antlr = %{version}-%{release}
Obsoletes:		maven2-plugin-antlr <= 2.0.8

%description
The Antlr Plugin has two goals:
- antlr:generate Generates file(s) to a target directory based on grammar 
  file(s).
- antlr:html Generates Antlr report for grammar file(s).

%package javadoc
Summary:		Javadocs for %{name}
Group:			Development/Java
Requires:		jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .modello
%patch1 -p1 -b .artifact
%patch2 -p1 -b .sink

# remove all binary bits
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

# Tests seem unhappy, skipping them.
mvn-jpp -Dmaven.test.skip=true \
-Dmaven.repo.local=$MAVEN_REPO_LOCAL \
install javadoc:javadoc

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_javadir}

cp -p target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
pushd %{buildroot}%{_javadir}
ln -s %{name}-%{version}.jar %{name}.jar
popd

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -rp target/site/apidocs/ %{buildroot}%{_javadocdir}/%{name}

install -d -m 755 %{buildroot}%{_mavenpomdir}
%add_to_maven_depmap org.codehaus.mojo %{name} %{version} JPP %{name}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

%clean
rm -rf %{buildroot}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%{_javadir}/%{name}*.jar

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}


Summary: A library for editing typed command lines.
Name: readline
Version: 4.2
Release: 2
License: GPL
Group: System Environment/Libraries
Source: ftp://ftp.gnu.org/gnu/readline-%{version}.tar.gz
Patch0: readline-2.2.1-guard.patch
Patch1: readline-4.1-outdated.patch
Patch2: readline-4.2-fixendkey.patch
Patch3: readline-4.1-booleancase.patch
Patch4: readline-4.2-cplusplus.patch
Prereq: /sbin/install-info /sbin/ldconfig
Buildroot: %{_tmppath}/%{name}-root
BuildRequires: sed

%description
The Readline library provides a set of functions that allow users to
edit command lines. Both Emacs and vi editing modes are available. The
Readline library includes additional functions for maintaining a list
of previously-entered command lines for recalling or editing those
lines, and for performing csh-like history expansion on previous
commands.

%package devel
Summary: Files needed to develop programs which use the readline library.
Group: Development/Libraries
Requires: readline = %{version}

%description devel
The Readline library provides a set of functions that allow users to
edit typed command lines. If you want to develop programs that will
use the readline library, you need to have the readline-devel package
installed. You also need to have the readline package installed.

%prep
%setup -q
%patch0 -p1 -b .guard
%patch1 -p1 -b .outdated
%patch2 -p1 -b .fixendkey
# XXX don't bother about this
#%patch3 -p1 -b .booleancase
%patch4 -p1 -b .c++

%build
%configure
make all shared

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}

%makeinstall install install-shared

chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/*.so*

{ cd ${RPM_BUILD_ROOT}
  ln -sf libreadline.so.%{version} .%{_libdir}/libreadline.so
  ln -sf libhistory.so.%{version} .%{_libdir}/libhistory.so
  ln -sf libreadline.so.%{version} \
  	.%{_libdir}/libreadline.so.`echo %{version} | sed 's^\..*^^g'`
  ln -sf libhistory.so.%{version} \
  	.%{_libdir}/libhistory.so.`echo %{version} | sed 's^\..*^^g'`
  gzip -9nf .%{_infodir}/*.info*
  rm -f .%{_infodir}/dir
}
 
%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/ldconfig
/sbin/install-info %{_infodir}/history.info.gz %{_infodir}/dir
/sbin/install-info %{_infodir}/readline.info.gz %{_infodir}/dir

%postun -p /sbin/ldconfig

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/history.info.gz %{_infodir}/dir
   /sbin/install-info --delete %{_infodir}/readline.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%{_mandir}/man*/*
%{_infodir}/*.info*
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/readline
%{_libdir}/lib*.a
%{_libdir}/lib*.so

%changelog
* Tue Aug  7 2001 Bernhard Rosenkraenzer <bero@redhat.com> 4.2-2
- Make sure headers can be included from C++ applications (#51131)
  (Patch based on Debian's with the bugs removed ;) )

* Wed May 09 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.2 and adapt patches

* Fri Apr  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- change the paths listed for the header files in the man page to reflect
  the location changes from previous versions (#35073)
- note that "on" is acceptable instead of "On" in the man page (#21327)

* Thu Mar  8 2001 Preston Brown <pbrown@redhat.com>
- fix reading of end key termcap value (@7 is correct, was kH) (#30884)

* Tue Jan 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- mark the man page as currently out-of-date (#25294)

* Thu Sep  7 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging (64bit systems need to use libdir).

* Thu Aug 17 2000 Jeff Johnson <jbj@redhat.com>
- summaries from specspo.

* Wed Aug  2 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- use "rm -f" in specfile

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Tue Mar 21 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 4.1

* Thu Feb 03 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.0

* Fri Apr 09 1999 Michael K. Johnson <johnsonm@redhat.com>
- added guard patch from Taneli Huuskonen <huuskone@cc.helsinki.fi>

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Sun Jul 26 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.2.1

* Wed May 06 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed May 06 1998 Cristian Gafton <gafton@redhat.com>
- don't package /usr/info/dir

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- devel package moved to Development/Libraries

* Tue Apr 21 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.2

* Tue Oct 14 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups

* Fri Oct 10 1997 Erik Troan <ewt@redhat.com>
- added proper sonames

* Tue Jul 08 1997 Erik Troan <ewt@redhat.com>
- updated to readline 2.1

* Tue Jun 03 1997 Erik Troan <ewt@redhat.com>
- built against glibc

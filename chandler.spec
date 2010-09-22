# TODO
# - source build: http://chandlerproject.org/Developers/ChandlerDesktopSource
# - nosource because not to trash df
Summary:	Note to self organizer
Name:		chandler
Version:	1.0.3
Release:	0.2
License:	Apache v2.0
Group:		Applications
Source0:	http://downloads.osafoundation.org/chandler/releases/%{version}/Chandler_hardy_%{version}-1_i386.deb
# NoSource0-md5:	f9df945f87a2b7c8e46c76b41a96d8b4
NoSource:	0
Source1:	http://downloads.osafoundation.org/chandler/releases/%{version}/Chandler_hardy_%{version}-1_amd64.deb
# NoSource1-md5:	843b00fc69c0074d0ed4544ea99e6c8f
NoSource:	1
URL:		http://www.chandlerproject.org/
Requires:	python-pyicu
Requires:	Zope-Interface
Requires:	python-M2Crypto
Requires:	python-dateutil
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages	0

%description
Manage and share events, calendars, and notes with a desktop
application Described as a "Note-to-Self Organizer", Chandler Desktop
provides a unique way to track calendars, tasks, and notes, each
placed into one or more collections and managed through a
now/later/done triage process. Collections can be shared either
read-only or with read-write access to multiple other people with
2-way sync and conflict detection. Both calendar and dashboard (list)
views are available for collections, and multiple collections can be
overlayed in the calendar view.

Chandler supports a variety of protocols, including IMAP/SMTP, CalDAV,
and iCalendar/ics over HTTP/HTTPS. You can point Chandler at your IMAP
account and drag items into Chandler using your existing IMAP client.
Using SMTP, Chandler can send event invitations and updates via
outbound email.

Using either CalDAV (for full 2-way synchronization) or ICS (1-way
subscribe or publish), you can overlay multiple calendars from almost
Internet-bases calendar source.

%prep
%setup -qcT
%ifarch %{ix86}
SOURCE=%{S:0}
%endif
%ifarch %{x8664}
SOURCE=%{S:1}
%endif

ar x $SOURCE
tar zxf control.tar.gz
tar zxf data.tar.gz

version=$(awk '/Version:/{print $2}' control)
if [ $version != %{version}-1 ]; then
	exit 1
fi

mv .%{_docdir}/chandler doc
mv .%{_datadir}/menu .

rm ./%{_pixmapsdir}/chandler-16.xpm
rm ./%{_pixmapsdir}/chandler.xpm
rm ./%{_iconsdir}/hicolor/scalable/apps/chandler.svg

grep -rl '#!.*bin/env python' . | xargs %{__sed} -i -e '1s,^#!.*python,#!%{__python},'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT
cp -a usr $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
# XXX temporarily
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/chandler
%dir %{_prefix}/lib/chandler
%{_prefix}/lib/chandler/*.py
%{_prefix}/lib/chandler/application
%{_prefix}/lib/chandler/chandler
%{_prefix}/lib/chandler/Chandler.egg-info
%{_prefix}/lib/chandler/i18n
%{_prefix}/lib/chandler/locale
%{_prefix}/lib/chandler/parcels
%{_prefix}/lib/chandler/plugins
%{_prefix}/lib/chandler/release
%{_prefix}/lib/chandler/tools
%{_prefix}/lib/chandler/util
%dir %{_datadir}/python-support
%{_datadir}/python-support/chandler.dirs

%{_mandir}/man1/chandler.1*
%{_desktopdir}/chandler.desktop
%{_pixmapsdir}/chandler.png
%{_iconsdir}/hicolor/*/apps/chandler.png

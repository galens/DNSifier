#!/usr/bin/python

import dnschef_lib
import sys
import os
import subprocess
import threading
import time
import types
from gi.repository import Gtk

class yaDNS(Gtk.Window):

    def __init__(self):
        # initialize starting variables
        self.tcp_val = False
        self.dns_running = False
        self.logfile = False
        self.hostfile = False
        self.CREATE_NO_WINDOW = 0x08000000

        self.dns_config = dict()
        self.dns_config['no dns override'] = dict()
        self.dns_config['no dns override']['A'] = dict()
        self.dns_config['no dns override']['A']['foo.bar'] = '127.0.0.1'
        self.dns_config['test01'] = dict()
        self.dns_config['test01']['A'] = dict()
        self.dns_config['test01']['A']['google.com'] = '127.0.0.1'
        self.dns_config['test01']['A']['yahoo.com'] = '127.0.0.2'
        self.dns_config['test01']['A']['msn.com'] = '127.0.0.3'
        
        self.dns_config['test02'] = dict()
        self.dns_config['test02']['A'] = dict()
        self.dns_config['test02']['A']['google.com'] = '127.0.0.4'
        self.dns_config['test02']['A']['yahoo.com'] = '127.0.0.5'
        self.dns_config['test02']['A']['msn.com'] = '127.0.0.6'
        
        self.dns_config['test03'] = dict()
        self.dns_config['test03']['A'] = dict()
        self.dns_config['test03']['A']['google.com'] = '127.0.0.7'
        self.dns_config['test03']['A']['yahoo.com'] = '127.0.0.8'
        self.dns_config['test03']['A']['msn.com'] = '127.0.0.9'


        self.nameserver = self.dns_config['test01'] # set default value in case no option is chosen

        Gtk.Window.__init__(self, title="DNSifier by: Galen Senogles")
        self.set_border_width(15)

        # stop user from resizing
        self.set_resizable(False)

        # set tooltip messages
        msg_enable_disable = "Turn the local DNS on or off"
        msg_choose_server  = "Select your server DNS override"
        msg_tcp_dns        = "Use TCP to make DNS calls instead of UDP"
        msg_external_dns   = "The external DNS to make calls to"
        msg_interface      = "The IP address to bind the DNS to"
        msg_log_file       = "Enter a filename to log actions to. Leave blank for no log"
        #msg_server_over    = "Enter a filename containing DNS entries to load"
        msg_toggle_dns     = "Use netsh to change local network to use DNS\nNote: Must be running as administrator"
        msg_obtain_dns     = "Use netsh to obtain current external DNS and update the field"
        msg_host_file      = "Specify a host file to load"

        self.box = Gtk.Box(spacing=6)
        self.add(self.box)
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.box.pack_start(self.listbox, True, True, 0)

        self.enab_row = Gtk.ListBoxRow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.enab_row.add(self.box)
        self.lbl_Switch = Gtk.Label("Enable/Disable", xalign=0)
        self.lbl_Switch.set_tooltip_text(msg_enable_disable)
        self.box.pack_start(self.lbl_Switch, True, True, 0)

        self.switch = Gtk.Switch()
        self.switch.set_tooltip_text(msg_enable_disable)
        self.switch.connect("notify::active", self.on_switch_activated)
        self.switch.set_active(False)
        self.box.pack_start(self.switch, True, True, 0)

        self.listbox.add(self.enab_row)

        self.server_row = Gtk.ListBoxRow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.server_row.add(self.box)
        self.lbl_Choice = Gtk.Label("Choose Server", xalign=0)
        self.lbl_Choice.set_tooltip_text(msg_choose_server)
        self.box.pack_start(self.lbl_Choice, True, True, 0)

        # drop down options
        self.servers = ['no dns override', 'test01', 'test02', 'test03']
        self.servers_combo = Gtk.ComboBoxText()
        self.servers_combo.set_tooltip_text(msg_choose_server)
        self.servers_combo.connect("changed", self.on_server_combo_changed)
        for s in self.servers:
            self.servers_combo.append_text(s)
        self.servers_combo.set_entry_text_column(0)
        self.box.pack_start(self.servers_combo, True, True, 0)

        self.listbox.add(self.server_row)

        self.check_row = Gtk.ListBoxRow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.check_row.add(self.box)
        self.lbl_Adv = Gtk.Label("Advanced Options", xalign=0)
        self.box.pack_start(self.lbl_Adv, True, True, 0)

        self.advanced_check = Gtk.CheckButton()
        self.advanced_check.set_active(False)
        self.advanced_check.connect("toggled", self.on_check_button_toggled)
        self.box.pack_start(self.advanced_check, False, False, 0)

        self.listbox.add(self.check_row)

        self.header_row1 = Gtk.ListBoxRow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.header_row1.add(self.box)
        self.lbl_header = Gtk.Label("", xalign=0)
        self.box.pack_start(self.lbl_header, True, True, 0)

        self.listbox.add(self.header_row1)

        self.header_row2 = Gtk.ListBoxRow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.header_row2.add(self.box)
        self.lbl_header = Gtk.Label("Program Options", xalign=0)
        self.box.pack_start(self.lbl_header, True, True, 0)

        self.listbox.add(self.header_row2)

        self.header_row3 = Gtk.ListBoxRow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.header_row3.add(self.box)
        self.lbl_header = Gtk.Label("", xalign=0)
        self.box.pack_start(self.lbl_header, True, True, 0)

        self.listbox.add(self.header_row3)

        self.prot_row = Gtk.ListBoxRow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.prot_row.add(self.box)
        self.lbl_prot = Gtk.Label("TCP DNS", xalign=0)
        self.lbl_prot.set_tooltip_text(msg_tcp_dns)
        self.box.pack_start(self.lbl_prot, True, True, 0)

        self.prot_check = Gtk.CheckButton()
        self.prot_check.set_tooltip_text(msg_tcp_dns)
        self.prot_check.set_active(False)
        self.prot_check.connect("toggled", self.on_check_prot_button_toggled)
        self.box.pack_start(self.prot_check, False, False, 0)

        self.listbox.add(self.prot_row)

        self.adv_row = Gtk.ListBoxRow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.adv_row.add(self.box)
        self.lbl_ext = Gtk.Label("External DNS", xalign=0)
        self.lbl_ext.set_tooltip_text(msg_external_dns)
        self.box.pack_start(self.lbl_ext, True, True, 0)

        self.dns_entry = Gtk.Entry()
        self.dns_entry.set_tooltip_text(msg_external_dns)
        self.dns_entry.set_width_chars(15)
        self.dns_entry.set_max_width_chars(15)
        self.dns_entry.set_text("8.8.8.8")
        self.box.pack_start(self.dns_entry, False, False, 0)

        self.listbox.add(self.adv_row)

        self.int_row = Gtk.ListBoxRow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.int_row.add(self.box)
        self.lbl_int = Gtk.Label("Interface", xalign=0)
        self.lbl_int.set_tooltip_text(msg_interface)
        self.box.pack_start(self.lbl_int, True, True, 0)

        self.local_interface = Gtk.Entry()
        self.local_interface.set_tooltip_text(msg_interface)
        self.local_interface.set_width_chars(15)
        self.local_interface.set_max_width_chars(15)
        self.local_interface.set_text("127.0.0.1")
        self.box.pack_start(self.local_interface, False, False, 0)

        self.listbox.add(self.int_row)

        self.log_row = Gtk.ListBoxRow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.log_row.add(self.box)
        self.lbl_log = Gtk.Label("Log File", xalign=0)
        self.lbl_log.set_tooltip_text(msg_log_file)
        self.box.pack_start(self.lbl_log, True, True, 0)

        self.log_path = Gtk.Entry()
        self.log_path.set_tooltip_text(msg_log_file)
        self.log_path.set_width_chars(15)
        self.log_path.set_max_width_chars(15)
        self.box.pack_start(self.log_path, False, False, 0)

        self.listbox.add(self.log_row)

        self.host_row = Gtk.ListBoxRow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.host_row.add(self.box)
        self.lbl_host = Gtk.Label("Host File", xalign=0)
        self.lbl_host.set_tooltip_text(msg_host_file)
        self.box.pack_start(self.lbl_host, True, True, 0)

        #self.host_path = Gtk.Entry()
        #self.host_path.set_tooltip_text(msg_host_file)
        #self.host_path.set_width_chars(15)
        #self.host_path.set_max_width_chars(15)
        #self.box.pack_start(self.host_path, False, False, 0)

        self.host_path = Gtk.Button("Choose File")
        self.host_path.set_tooltip_text(msg_host_file)
        self.host_path.connect("clicked", self.on_host_clicked)
        self.box.pack_start(self.host_path, False, False, 0)

        self.listbox.add(self.host_row)

        self.footer_row1 = Gtk.ListBoxRow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.footer_row1.add(self.box)
        self.lbl_header = Gtk.Label("", xalign=0)
        self.box.pack_start(self.lbl_header, True, True, 0)

        self.listbox.add(self.footer_row1)

        self.footer_row2 = Gtk.ListBoxRow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.footer_row2.add(self.box)
        self.lbl_header = Gtk.Label("Windows Options", xalign=0)
        self.box.pack_start(self.lbl_header, True, True, 0)

        self.listbox.add(self.footer_row2)

        self.footer_row3 = Gtk.ListBoxRow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.footer_row3.add(self.box)
        self.lbl_header = Gtk.Label("", xalign=0)
        self.box.pack_start(self.lbl_header, True, True, 0)

        self.listbox.add(self.footer_row3)

        self.update_row = Gtk.ListBoxRow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.update_row.add(self.box)
        self.lbl_net = Gtk.Label("Toggle local network\ninterface to use DNS", xalign=0)
        self.lbl_net.set_tooltip_text(msg_toggle_dns)
        self.box.pack_start(self.lbl_net, True, True, 0)

        self.network_button = Gtk.ToggleButton('Enable')
        self.network_button.set_tooltip_text(msg_toggle_dns)
        self.network_button.connect("toggled", self.on_network_button_toggled)
        self.box.pack_start(self.network_button, False, False, 0)

        self.listbox.add(self.update_row)

        self.update2_row = Gtk.ListBoxRow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.update2_row.add(self.box)
        self.lbl_dns = Gtk.Label("Obtain current DNS", xalign=0)
        self.lbl_dns.set_tooltip_text(msg_obtain_dns)
        self.box.pack_start(self.lbl_dns, True, True, 0)

        self.grab_button = Gtk.Button.new_with_label('Obtain')
        self.grab_button.set_tooltip_text(msg_obtain_dns)
        self.grab_button.connect("clicked", self.on_grab_button_clicked)
        self.box.pack_start(self.grab_button, False, False, 0)

        self.listbox.add(self.update2_row)

    def which(self, program):
      import os
      def is_exe(fpath):
          return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

      fpath, fname = os.path.split(program)
      if fpath:
          if is_exe(program):
              return program
      else:
          for path in os.environ["PATH"].split(os.pathsep):
              path = path.strip('"')
              exe_file = os.path.join(path, program)
              if is_exe(exe_file):
                  return exe_file
      return False

    def isUserAdmin(self):
      if os.name == 'nt':
          import ctypes
          # WARNING: requires Windows XP SP2 or higher!
          try:
              return ctypes.windll.shell32.IsUserAnAdmin()
          except:
              traceback.print_exc()
              print "Admin check failed, assuming not an admin."
              return False
      elif os.name == 'posix':
          # Check for root on Posix
          return os.getuid() == 0
      else:
          raise RuntimeError, "Unsupported operating system for this module: %s" % (os.name,)

    def runAsAdmin(self, cmdLine=None, wait=True):
        if os.name != 'nt':
            raise RuntimeError, "This function is only implemented on Windows."

        import win32api, win32con, win32event, win32process
        from win32com.shell.shell import ShellExecuteEx
        from win32com.shell import shellcon

        python_exe = sys.executable

        if cmdLine is None:
            cmdLine = [python_exe] + sys.argv
        elif type(cmdLine) not in (types.TupleType,types.ListType):
            raise ValueError, "cmdLine is not a sequence."
        cmdLine = cmdLine[0].split()
        cmd = '"%s"' % (cmdLine[0],)
        # XXX TODO: isn't there a function or something we can call to massage command line params?
        params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
        cmdDir = ''
        #showCmd = win32con.SW_SHOWNORMAL
        showCmd = win32con.SW_HIDE
        lpVerb = 'runas'  # causes UAC elevation prompt.

        # print "Running", cmd, params

        # ShellExecute() doesn't seem to allow us to fetch the PID or handle
        # of the process, so we can't get anything useful from it. Therefore
        # the more complex ShellExecuteEx() must be used.

        # procHandle = win32api.ShellExecute(0, lpVerb, cmd, params, cmdDir, showCmd)

        try:
            procInfo = ShellExecuteEx(nShow=showCmd,
                                  fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                                  lpVerb=lpVerb,
                                  lpFile=cmd,
                                  lpParameters=params)

            if wait:
                procHandle = procInfo['hProcess']
                obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
                rc = win32process.GetExitCodeProcess(procHandle)
                #print "Process handle %s returned code %s" % (procHandle, rc)
            else:
                rc = None
            return rc
        except:
            self.log_action(self.logfile, "There was an error attempting to update your local network settings. Please do so manually.")
            self.network_button.set_inconsistent(True)
            self.network_button.set_label('Enable')
            return None

    def on_grab_button_clicked(self, button):
        ext_dns = self.update_local_network_dns('Lookup')
        if ext_dns:
          self.dns_entry.set_text(ext_dns)

    def update_local_network_dns(self, toggle):
        interface_cmd = subprocess.check_output(["netsh", "interface", "show", "interface"], shell=False, creationflags=self.CREATE_NO_WINDOW)
        interface_split = interface_cmd.split("\r\n")
        for row in interface_split:
            if 'Enabled' in row and 'Connected' in row and 'VirtualBox' not in row:
                active_connection_row = row.split()
                if len(active_connection_row) > 4:
                    active_connection = ' '.join(active_connection_row[3:])
                else:
                    active_connection = row.split()[-1]
        if active_connection:
            try:
                if toggle == 'Enable':
                    if not self.isUserAdmin():
                      netsh_path = self.which('netsh.exe')
                      if netsh_path:
                        full_cmd = '%s interface ip set dns "%s" static %s' % (netsh_path, active_connection, self.local_interface.get_text())
                        self.runAsAdmin([full_cmd])
                      else:
                        subprocess.check_output(["netsh", "interface", "ip", "set", "dns", "\"%s\"" % active_connection, "static", "127.0.0.1"], shell=False, creationflags=self.CREATE_NO_WINDOW)
                      self.log_action(self.logfile, "Enabling local network interface DNS")
                elif toggle == 'Disable':
                    if not self.isUserAdmin():
                      netsh_path = self.which('netsh.exe')
                      if netsh_path:
                        full_cmd = '%s interface ip set dns %s dhcp' % (netsh_path, active_connection)
                        self.runAsAdmin([full_cmd])
                    else:
                         subprocess.check_output(["netsh", "interface", "ip", "set", "dns", "\"%s\"" % active_connection, "dhcp"],shell=False, creationflags=self.CREATE_NO_WINDOW)
                         self.log_action(self.logfile, "Disabling local network interface DNS")
                elif toggle == 'Lookup':
                    dns_list = ['DNS servers configured through DHCP', 'Statically Configured DNS Servers']
                    self.log_action(self.logfile, "Grabbing current DNS")
                    cur_dns = subprocess.check_output(["netsh", "interface", "ip", "show", "dns", "\"%s\"" % active_connection], shell=False, creationflags=self.CREATE_NO_WINDOW)
                    if cur_dns:
                        cur_dns_split = cur_dns.split("\r\n")
                        for row in cur_dns_split:
                            for list in dns_list:
                                if list in row:
                                    row_split = row.split(":")
                                    return row_split[1].strip()
                        return False
            except OSError as e:
                self.log_action(self.logfile, "Error: %s" % e)
                return False
            except subprocess.CalledProcessError as e:
                self.log_action(self.logfile, "Error: %s" % e)
                return False

    def on_network_button_toggled(self, button):
        if button.get_active():
            state = 'on'
            button.set_label('Disable')
            self.update_local_network_dns('Enable')
        else:
            state = 'off'
            button.set_label('Enable')
            self.update_local_network_dns('Disable')
        print('button was turned', state)

    def show_advanced_options(self):
        self.adv_row.show()
        self.prot_row.show()
        self.int_row.show()
        self.log_row.show()
        self.host_row.show()
        #self.ovr_row.show()
        self.header_row1.show()
        self.header_row2.show()
        self.header_row3.show()
        self.footer_row1.show()
        self.footer_row2.show()
        self.footer_row3.show()
        self.update_row.show()
        self.update2_row.show()

    def remove_advanced_options(self):
        self.adv_row.hide()
        self.prot_row.hide()
        self.int_row.hide()
        self.log_row.hide()
        self.host_row.hide()
        #self.ovr_row.hide()
        self.header_row1.hide()
        self.header_row2.hide()
        self.header_row3.hide()
        self.footer_row1.hide()
        self.footer_row2.hide()
        self.footer_row3.hide()
        self.update_row.hide()
        self.update2_row.hide()
        self.dynamic_window_resize()

    def initial_show(self):
        win.show_all()
        self.remove_advanced_options()

    def dynamic_window_resize(self):
        win.resize(1, 1)

    def log_action(self, logfile, message):
        if logfile:
            self.log = open(logfile,'a',0)
            self.log.write("[%s] %s.\n" % (time.strftime("%d/%b/%Y:%H:%M:%S %z"), message))
            return self.log
        else:
            print message
            return None

    def flush_dns(self):
        interface_cmd = subprocess.check_output(["ipconfig", "/flushdns"], shell=False, creationflags=self.CREATE_NO_WINDOW)
        interface_split = interface_cmd.split("\r\n")
        for row in interface_split:
            if 'Successfully flushed' in row and 'DNS' in row:
                return True

    def process_host(self, hostfile):
        self.log_action(self.logfile, "Attempting to process external hostfile: %s" % (hostfile))
        if os.path.isfile(hostfile):
          self.servers = []
          tmp = []
          self.dns_config = dict()
          self.servers_combo.remove_all()
          self.dns_config['no dns override'] = dict()
          self.dns_config['no dns override']['A'] = dict()
          self.dns_config['no dns override']['A']['foo.bar'] = '127.0.0.1'
          self.servers.append('no dns override')
          with open(hostfile, 'r') as f:
            i = 0
            j = 1
            for line in f:
              if line[:1] != '#' and line.split():
                self.servers.append(line.rstrip())
                self.dns_config[self.servers[-1]] = dict()
                self.dns_config[self.servers[-1]]['A'] = dict()
              elif line[:1] == '#':
                line = line[1:]
                list_line = line.split()
                for column in list_line[1:]:
                  self.dns_config[self.servers[-1]]['A'][column] = list_line[0]
                  #print 'self.dns_config_%s[\'A\'][\'%s\'] = \'%s\'' % (j, column, list_line[0])
              else:
                j +=1
              i += 1

          for s in self.servers:
            self.servers_combo.append_text(s)
          self.servers_combo.set_entry_text_column(0)
          self.log_action(self.logfile, 'Host file successfully processed!')
          return True
        else:
          self.log = self.log_action(self.logfile, 'There was a problem processing your host file, exiting')
          exit()

    def on_switch_activated(self, switch, gparam):
        global server
        tree_iter = self.servers_combo.get_active_iter()
        if tree_iter != None:
            if switch.get_active():
                state = "on"
                self.dns_running = True
                interface = self.local_interface.get_text()
                nameserver = self.dns_entry.get_text()
                nameservers = dnschef_lib.returnNameServers(nameserver)
                self.logfile = self.log_path.get_text()

                ipv6=False
                port='53'

                self.log = self.log_action(self.logfile, 'DNSifier is active')

                try:
                    print self.nametodns
                    if self.tcp_val:
                        self.log_action(self.logfile, "DNSifier is running in TCP mode")
                        self.server = dnschef_lib.ThreadedTCPServer((interface, int(port)), dnschef_lib.TCPHandler, self.nametodns, nameservers, ipv6, self.log)
                    else:
                        self.log_action(self.logfile, "DNSifier is running in UDP mode")
                        self.server = dnschef_lib.ThreadedUDPServer((interface, int(port)), dnschef_lib.UDPHandler, self.nametodns, nameservers, ipv6, self.log)

                    # Start a thread with the server -- that thread will then start more threads for each request
                    server_thread = threading.Thread(target=self.server.serve_forever)

                    # Exit the server thread when the main thread terminates
                    server_thread.daemon = True
                    server_thread.start()

                    # flush da dns oyy
                    self.flush_dns()

                except (KeyboardInterrupt, SystemExit):
                    server.shutdown()
                    self.log_action(self.logfile, "DNSifier is shutting down")
                    sys.exit()

                except IOError:
                    print "[!] Failed to open log file for writing."

                except Exception, e:
                    error = "[!] Failed to start the server: %s" % e
                    self.log_action(self.logfile, error)
            else:
                state = "off"
                self.shutdown_server()
            print("Switch was turned", state)
        else:
            self.switch.set_active(False)

    def shutdown_server(self):
        self.dns_running = False
        self.log_action(self.logfile, "DNSifier is shutting down")
        self.server.shutdown()
        self.server.server_close()
        self.switch.set_active(False)

    def shutdown_if_running(self):
        if self.dns_running == True:
           self.shutdown_server()

    def on_server_combo_changed(self, combo):
        text = combo.get_active_text()
        if text:
          returned_dict = self.dns_config.get(text)
          if returned_dict:
            self.nametodns = returned_dict

          if text != None:
              print("Selected: server=%s" % text)

          self.shutdown_if_running()
          time.sleep(1)
          self.switch.set_active(True)
          self.flush_dns()

    def on_check_button_toggled(self, checkbutton):
        if checkbutton.get_active():
            self.show_advanced_options()
            print("Checkbutton toggled on")
        else:
            self.remove_advanced_options()
            print("Checkbutton toggled off")

    def on_check_prot_button_toggled(self, checkbutton):
        if checkbutton.get_active():
            self.tcp_val = True
            print("Switching to TCP DNS proxy")
        else:
            self.tcp_val = False
            print("Switching to default UDP DNS proxy")

        self.shutdown_if_running()

    def on_host_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            self.process_host(dialog.get_filename())

        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
        dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)


win = yaDNS()
win.connect("delete-event", Gtk.main_quit)
win.initial_show()
Gtk.main()
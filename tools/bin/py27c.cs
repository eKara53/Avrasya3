using System;
using System.IO;
using System.Runtime.InteropServices;

class Program {
    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Ansi)]
    static extern IntPtr LoadLibrary(string lpFileName);

    [DllImport("python27.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern void Py_Initialize();

    [DllImport("python27.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern int PyRun_SimpleString(string command);

    [DllImport("python27.dll", CallingConvention = CallingConvention.Cdecl)]
    static extern void Py_Finalize();

    static int Main(string[] args) {
        if (args.Length < 2) {
            Console.Error.WriteLine("Usage: py27c [client_dir] [src.py] [dst.pyc] | py27c [client_dir] --sim");
            return 1;
        }
        string clientDir = args[0];
        Environment.CurrentDirectory = clientDir;
        IntPtr h = LoadLibrary(Path.Combine(clientDir, "python27.dll"));
        if (h == IntPtr.Zero) {
            Console.Error.WriteLine("Failed to load python27.dll");
            return 2;
        }
        Py_Initialize();

        if (args[1] == "--sim") {
            string simCmd =
                "import sys, imp\n" +
                "# 1.Sahte C motor modullerini olustur (prototype.py satir 7'de ekran=0, satir 28'de ekran=1920)\n" +
                "wndMgr = imp.new_module('wndMgr')\n" +
                "wndMgr._w = 0\n" +
                "wndMgr.GetScreenWidth = lambda: wndMgr._w\n" +
                "wndMgr.GetScreenHeight = lambda: 1080\n" +
                "sys.modules['wndMgr'] = wndMgr\n" +
                "grp = imp.new_module('grp')\n" +
                "grp.GenerateColor = lambda r, g, b, a: 0xFF112233\n" +
                "sys.modules['grp'] = grp\n" +
                "# 2. Avrasya2 system.py davranisini birebir taklit et:\n" +
                "sys.path = ['lib']\n" +
                "old_import = __import__\n" +
                "module_do = lambda x: None\n" +
                "ui_src = '''\n" +
                "class Window(object):\n" +
                "    def __init__(self, layer='UI'): self.layer = layer\n" +
                "    def SetSize(self, w, h): pass\n" +
                "    def SetPosition(self, x, y): pass\n" +
                "    def SetParent(self, p): pass\n" +
                "    def AddFlag(self, f): pass\n" +
                "    def SetTop(self): pass\n" +
                "    def Show(self): pass\n" +
                "    def Hide(self): pass\n" +
                "class Bar(Window):\n" +
                "    def SetColor(self, c): pass\n" +
                "class TextLine(Window):\n" +
                "    def SetText(self, t): self.text = t\n" +
                "'''\n" +
                "def __hybrid_import(name, globals=None, locals=None, fromlist=None, level=-1):\n" +
                "    if name == 'ui':\n" +
                "        if 'ui' in sys.modules: return sys.modules['ui']\n" +
                "        m = imp.new_module('ui')\n" +
                "        sys.modules['ui'] = m\n" +
                "        exec compile(ui_src, 'ui.py', 'exec') in m.__dict__\n" +
                "        module_do(m)\n" +
                "        return m\n" +
                "    return old_import(name, globals, locals, fromlist)\n" +
                "import __builtin__\n" +
                "__builtin__.__import__ = __hybrid_import\n" +
                "# 3. prototype.py satir 7: ekran henuz 0 iken pack uzerinden ui import edilir\n" +
                "import ui\n" +
                "# 4. prototype.py satir 28: wndMgr.SetScreenSize cagirilir\n" +
                "wndMgr._w = 1920\n" +
                "# 5. prototype.py satir 49: mainStream.Create() -> PhaseCurtain(ui.Bar) olusturulur\n" +
                "class PhaseCurtain(ui.Bar):\n" +
                "    def __init__(self):\n" +
                "        ui.Bar.__init__(self, 'CURTAIN')\n" +
                "curtain = PhaseCurtain()\n" +
                "ctl = getattr(sys, '_ui_frame_ctl', None)\n" +
                "if ctl is None:\n" +
                "    raise RuntimeError('HATA: _ui_frame_ctl yuklenmedi!')\n" +
                "ctl.on_update()\n" +
                "print('SIMULASYON BASARILI: _ui_frame_ctl=' + str(type(ctl)) + ', kare=' + str(ctl.frames) + ', hud_satir0=' + str(ctl.hud.lines[0].text))\n";
            int simRc = PyRun_SimpleString(simCmd);
            Py_Finalize();
            return simRc;
        }

        string src = Path.GetFullPath(args[1]).Replace("\\", "/");
        string dst = Path.GetFullPath(args[2]).Replace("\\", "/");
        string cmd =
            "import imp, marshal\n" +
            "f = open(r'" + src + "', 'rb')\n" +
            "src_bytes = f.read().replace('\\r\\n', '\\n')\n" +
            "f.close()\n" +
            "code = compile(src_bytes, r'" + src + "', 'exec')\n" +
            "out = open(r'" + dst + "', 'wb')\n" +
            "out.write(imp.get_magic() + '\\x00\\x00\\x00\\x00' + marshal.dumps(code))\n" +
            "out.close()\n";
        int rc = PyRun_SimpleString(cmd);
        Py_Finalize();
        return rc;
    }
}

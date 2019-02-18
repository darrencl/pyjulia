import sys

import pytest

from .test_compatible_exe import runcode


@pytest.mark.xfail(reason="https://github.com/JuliaPy/PyCall.jl/pull/648")
def test_compiled_modules_no():
    runcode(
        sys.executable,
        """
        from julia.core import Julia

        Julia(debug=True, compiled_modules=False)

        from julia import Main
        use_compiled_modules = Main.eval("Base.JLOptions().use_compiled_modules")

        print("use_compiled_modules =", use_compiled_modules)
        assert use_compiled_modules == 0
        """,
        check=True)


def test_custom_sysimage(tmpdir):
    sysimage = str(tmpdir.join("sys.so"))
    runcode(
        sys.executable,
        """
        from shutil import copyfile
        from julia.core import LibJulia, JuliaInfo, enable_debug

        enable_debug()
        info = JuliaInfo.load()

        sysimage = {!r}
        copyfile(info.image_file, sysimage)

        api = LibJulia.load()
        api.init_julia(["--sysimage", sysimage])

        from julia import Main
        actual = Main.eval("unsafe_string(Base.JLOptions().image_file)")

        print("actual =", actual)
        print("sysimage =", sysimage)
        assert actual == sysimage
        """.format(sysimage),
        check=True)

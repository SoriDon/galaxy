import os
from shutil import rmtree
from tempfile import mkdtemp

from galaxy.tool_util.loader import load_tool, template_macro_params
from galaxy.tool_util.unittest_utils.sample_data import SIMPLE_MACRO, SIMPLE_TOOL_WITH_MACRO
from galaxy.util import parse_xml, xml_to_string


def test_loader():

    class TestToolDirectory:
        __test__ = False  # Prevent pytest from discovering this class (issue #12071)

        def __init__(self):
            self.temp_directory = mkdtemp()

        def __enter__(self):
            return self

        def __exit__(self, type, value, tb):
            rmtree(self.temp_directory)

        def write(self, contents, name="tool.xml"):
            open(os.path.join(self.temp_directory, name), "w").write(contents)

        def load(self, name="tool.xml", preprocess=True):
            path = os.path.join(self.temp_directory, name)
            if preprocess:
                return load_tool(path)
            else:
                return parse_xml(path)

    # Test simple macro replacement.
    with TestToolDirectory() as tool_dir:
        tool_dir.write('''
<tool>
    <expand macro="inputs" />
    <macros>
        <macro name="inputs">
            <inputs />
        </macro>
    </macros>
</tool>''')
        xml = tool_dir.load(preprocess=False)
        assert xml.find("inputs") is None
        xml = tool_dir.load(preprocess=True)
        assert xml.find("inputs") is not None

    # Test importing macros from external files
    with TestToolDirectory() as tool_dir:
        tool_dir.write(SIMPLE_TOOL_WITH_MACRO)

        tool_dir.write(SIMPLE_MACRO.substitute(tool_version="2.0"), name="external.xml")
        xml = tool_dir.load(preprocess=False)
        assert xml.find("inputs") is None
        xml = tool_dir.load(preprocess=True)
        assert xml.find("inputs") is not None

    # Test macros with unnamed yield statements.
    with TestToolDirectory() as tool_dir:
        tool_dir.write('''
<tool>
    <expand macro="inputs">
        <input name="first_input" />
    </expand>
    <expand macro="inputs">
        <input name="second_input" />
    </expand>
    <expand macro="inputs">
        <input name="third_input" />
    </expand>
    <macros>
        <macro name="inputs">
            <expand macro="foo">
                <yield />
            </expand>
        </macro>
        <macro name="foo">
            <inputs>
                <yield />
            </inputs>
        </macro>
    </macros>
</tool>''')
        xml = tool_dir.load()
        assert xml.find("/inputs[1]/input").get("name") == "first_input"
        assert xml.find("/inputs[2]/input").get("name") == "second_input"
        assert xml.find("/inputs[3]/input").get("name") == "third_input"

    # Test nested macro with yield statements
    with TestToolDirectory() as tool_dir:
        tool_dir.write("""
<tool>
    <macros>
        <macro name="paired_options">
            <when value="paired">
                <yield />
            </when>
            <when value="paired_collection">
                <yield />
            </when>
        </macro>
        <macro name="single_or_paired_general">
            <conditional name="library">
                <expand macro="paired_options">
                    <yield />
                </expand>
            </conditional>
        </macro>
    </macros>
    <inputs>
        <expand macro="single_or_paired_general">
            <param name="test"/>
        </expand>
    </inputs>
</tool>
""")
        xml = tool_dir.load()
        # assert the both yields in the inner macro (paired_options) are expanded
        assert xml.find('/inputs/conditional[@name="library"]/when[@value="paired"]/param[@name="test"]') is not None
        assert xml.find('/inputs/conditional[@name="library"]/when[@value="paired_collection"]/param[@name="test"]') is not None

    # Test recursive macro applications.
    with TestToolDirectory() as tool_dir:
        tool_dir.write('''
<tool>
    <expand macro="inputs">
        <input name="first_input" />
        <expand macro="second" />
    </expand>
    <macros>
        <macro name="inputs">
            <inputs>
                <yield />
                <input name="third_input" />
            </inputs>
        </macro>
        <macro name="second">
            <input name="second_input" />
        </macro>
    </macros>
</tool>''')
        xml = tool_dir.load()
        assert xml.find("/inputs/input[1]").get("name") == "first_input"
        assert xml.find("/inputs/input[2]").get("name") == "second_input"
        assert xml.find("/inputs/input[3]").get("name") == "third_input"

    # Test recursive macro applications.
    with TestToolDirectory() as tool_dir:
        tool_dir.write('''
<tool>
    <expand macro="inputs">
        <input name="first_input" />
        <expand macro="second" />
    </expand>
    <macros>
        <macro name="inputs">
            <inputs>
                <yield />
            </inputs>
        </macro>
        <macro name="second">
            <expand macro="second_delegate" />
            <input name="third_input" />
        </macro>
        <macro name="second_delegate">
            <input name="second_input" />
        </macro>
    </macros>
</tool>''')
        xml = tool_dir.load()
        assert xml.find("/inputs/input[1]").get("name") == "first_input"
        assert xml.find("/inputs/input[2]").get("name") == "second_input"
        assert xml.find("/inputs/input[3]").get("name") == "third_input"

    # test expansion of top level (ie child of <macro>) yields
    with TestToolDirectory() as tool_dir:
        tool_dir.write('''
<tool id="issue_647">
    <macros>
        <macro name="a">
            <param name="a1" type="text" value="a1" label="a1"/>
            <yield />
        </macro>
    </macros>
    <inputs>
        <expand macro="a">
            <param name="b" type="text" value="b" label="b" />
        </expand>
    </inputs>
</tool>''')
        xml = tool_dir.load()
        assert xml.find("/inputs/param[1]").get("name") == "a1"
        assert xml.find("/inputs/param[2]").get("name") == "b"

    # Test <xml> is shortcut for macro type="xml"
    with TestToolDirectory() as tool_dir:
        tool_dir.write('''
<tool>
    <expand macro="inputs" />
    <macros>
        <xml name="inputs">
            <inputs />
        </xml>
    </macros>
</tool>''')
        xml = tool_dir.load()
        assert xml.find("inputs") is not None

    with TestToolDirectory() as tool_dir:
        tool_dir.write('''
<tool>
    <command interpreter="python">tool_wrapper.py
    #include source=$tool_params
    </command>
    <macros>
        <template name="tool_params">-a 1 -b 2</template>
    </macros>
</tool>
''')
        xml = tool_dir.load()
        params_dict = template_macro_params(xml.getroot())
        assert params_dict['tool_params'] == "-a 1 -b 2"

    with TestToolDirectory() as tool_dir:
        tool_dir.write('''
<tool>
    <macros>
        <token name="@CITATION@">The citation.</token>
    </macros>
    <help>@CITATION@</help>
    <another>
        <tag />
    </another>
</tool>
''')
        xml = tool_dir.load()
        help_el = xml.find("help")
        assert help_el.text == "The citation.", help_el.text

    with TestToolDirectory() as tool_dir:
        tool_dir.write('''
<tool>
    <macros>
        <token name="@TAG_VAL@">The value.</token>
    </macros>
    <another>
        <tag value="@TAG_VAL@" />
    </another>
</tool>
''')
        xml = tool_dir.load()
        assert xml.find('/another/tag[@value="The value."]') is not None

    with TestToolDirectory() as tool_dir:
        tool_dir.write('''
<tool>
    <macros>
        <token name="@TAG_VAL@"><![CDATA[]]></token>
    </macros>
    <another>
        <tag value="@TAG_VAL@" />
    </another>
</tool>
''')
        xml = tool_dir.load()
        assert xml.find('/another/tag[@value=""]') is not None

    # Test macros XML macros with $$ expansions in attributes
    with TestToolDirectory() as tool_dir:
        tool_dir.write('''
<tool>
    <expand macro="inputs" bar="hello" />
    <expand macro="inputs" bar="my awesome" />
    <expand macro="inputs" bar="doggo" />
    <macros>
        <xml name="inputs" tokens="bar" token_quote="$$">
            <inputs type="the type is $$BAR$$" />
        </xml>
    </macros>
</tool>
''')
        xml = tool_dir.load()
        input_els = xml.findall("inputs")
        assert len(input_els) == 3
        assert input_els[0].attrib["type"] == "the type is hello"
        assert input_els[1].attrib["type"] == "the type is my awesome"
        assert input_els[2].attrib["type"] == "the type is doggo"

    # Test macros XML macros with @ expansions in text
    with TestToolDirectory() as tool_dir:
        tool_dir.write('''
<tool>
    <expand macro="inputs" foo="hello" />
    <expand macro="inputs" foo="world" />
    <expand macro="inputs" />
    <macros>
        <xml name="inputs" token_foo="the_default">
            <inputs>@FOO@</inputs>
        </xml>
    </macros>
</tool>
''')
        xml = tool_dir.load()
        input_els = xml.findall("inputs")
        assert len(input_els) == 3
        assert input_els[0].text == "hello"
        assert input_els[1].text == "world"
        assert input_els[2].text == "the_default"

    # Test macros XML macros with @ expansions and recursive
    with TestToolDirectory() as tool_dir:
        tool_dir.write('''
<tool>
    <expand macro="inputs" foo="hello" />
    <expand macro="inputs" foo="world" />
    <expand macro="inputs" />
    <macros>
        <xml name="inputs" token_foo="the_default">
            <expand macro="real_inputs"><cow>@FOO@</cow></expand>
        </xml>
        <xml name="real_inputs">
            <inputs><yield /></inputs>
        </xml>
    </macros>
</tool>
''')
        xml = tool_dir.load()
        input_els = xml.findall("inputs")
        assert len(input_els) == 3
        assert input_els[0].find("cow").text == "hello"
        assert input_els[1].find("cow").text == "world"
        assert input_els[2].find("cow").text == "the_default"

    # test expansion of named and unnamed yield
    # - named yields are replaced by content of the corresponding token
    # - unnamed yields are replaced by all non-token elements of the expand tag
    with TestToolDirectory() as tool_dir:
        tool_dir.write('''
<tool>
    <macros>
        <xml name="test">
            <A>
                <yield/>
            </A>
            <yield name="token1"/>
            <B>
                <yield/>
                <yield name="token2"/>
            </B>
        </xml>
    </macros>
    <expand macro="test">
        <token name="token1">
            <content_of_token1/>
            <more_content_of_token1/>
        </token>
        <sub_of_expand_1/>
        <token name="token2">
            <content_of_token2/>
            <more_content_of_token2/>
        </token>
        <sub_of_expand_2/>
    </expand>
</tool>
''')
        xml = tool_dir.load()
        assert xml_to_string(xml, pretty=True) == '''<?xml version="1.0" ?>
<tool>
    <macros>
        </macros>
    <A>
        <sub_of_expand_1/>
        <sub_of_expand_2/>
    </A>
    <content_of_token1/>
    <more_content_of_token1/>
    <B>
        <sub_of_expand_1/>
        <sub_of_expand_2/>
        <content_of_token2/>
        <more_content_of_token2/>
    </B>
</tool>'''

    # test replacement of multiple top level yield
    with TestToolDirectory() as tool_dir:
        tool_dir.write('''
<tool>
    <macros>
        <xml name="test">
            <blah/>
            <yield/>
            <blah>
                <yield name="token1"/>
            </blah>
            <yield name="token2"/>
        </xml>
    </macros>
    <expand macro="test">
        <token name="token1">
            <content_of_token1/>
            <more_content_of_token1/>
        </token>
        <sub_of_expand_1/>
        <token name="token2">
            <content_of_token2/>
            <more_content_of_token2/>
        </token>
        <sub_of_expand_2/>
    </expand>
</tool>
''')
        xml = tool_dir.load()
        assert xml_to_string(xml, pretty=True) == '''<?xml version="1.0" ?>
<tool>
    <macros>
        </macros>
    <blah/>
    <sub_of_expand_1/>
    <sub_of_expand_2/>
    <blah>
        <content_of_token1/>
        <more_content_of_token1/>
    </blah>
    <content_of_token2/>
    <more_content_of_token2/>
</tool>'''

    # test 'recursive' replacement with named yields
    # since named yields are processed in order of the definition of the
    # corresponding tokens:
    # - replacing yield for token1 introduces yield for token2
    # - replacing yield for token2 introduced unnamed yield
    # - replacing unnamed yield gives the only non-token element of the expand
    with TestToolDirectory() as tool_dir:
        tool_dir.write('''
<tool>
    <macros>
        <xml name="test">
            <A>
                <yield name="token1"/>
            </A>
        </xml>
    </macros>
    <expand macro="test">
        <token name="token1">
            <T1>
                <yield name="token2"/>
            </T1>
        </token>
        <token name="token2">
            <T2>
                <yield/>
            </T2>
        </token>
        <T/>
    </expand>
</tool>''')

        xml = tool_dir.load()
        print(xml_to_string(xml, pretty=True))
        assert xml_to_string(xml, pretty=True) == '''<?xml version="1.0" ?>
<tool>
    <macros>
        </macros>
    <A>
        <T1>
            <T2>
                <T/>
            </T2>
        </T1>
    </A>
</tool>'''

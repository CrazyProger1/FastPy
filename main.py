from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('cpp_code')
env = Environment(loader=file_loader)

internal_code = '''
log("Hello, World!");
test();
'''

external_code = '''
void test(){
    log_error("Test Error");
}
'''

includes = '''
#include<curl>
'''

minimal = env.get_template('minimal.cpp')
print(minimal.render(internal_code=internal_code, external_code=external_code, additional_includes=includes))

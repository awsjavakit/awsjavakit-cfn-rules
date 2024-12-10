from assertpy import assert_that

from src import hello



class HandlerTest:

    def should_return_hello(self):
        assert_that(hello.hello()).is_equal_to("hello world")

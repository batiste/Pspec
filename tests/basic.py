from spec import expect, Spec

class MySpec(Spec):

    def it_should_be_correct(self):
        expect(1).to_equal(1)

    def it_should_be_incorrect(self):
        expect(1).to_not_equal(2)

def it_should_be_correct():
    expect(1).to_equal(1).to_not_equal(2)

def it_should_be_not_correct():
    expect(2).to_not_equal(1)


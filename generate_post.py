import datetime

def write_to_file(fname, s):
    f = open(fname, 'w')
    f.write(s)
    f.close()

def create_post(post_name):
    body = '''Testing
<br>
<br>
*This post was automatically generated by Augury.*
    '''

    s = '''---
layout: post
time: {}
---

{}'''.format(datetime.datetime.now().strftime('%I:%M %p'), body)

    post_name = '-'.join(post_name.split(' '))

    write_to_file('web/_posts/{}-{}.md'.format(datetime.datetime.now().strftime('%Y-%m-%d'), post_name), s)


if __name__ == '__main__':
    create_post('General Motors')
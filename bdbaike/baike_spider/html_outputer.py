class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        fout = open('output.html', 'w')

        fout.write('<html><head><meta charset="UTF-8"></head>')
        fout.write("<body>")
        fout.write("<table>")
        for data in self.datas:
            fout.write("<tr>")
            print 'url:', data['url']
            fout.write("<td>%s</td>" % data['url'])
            print 'title:', data['title']
            fout.write("<td>%s</td>" % data['title'])
            print 'summary:', data['summary']
            fout.write("<td>%s</td>" % data['summary'])
            fout.write("</tr>")
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")

import Image
import ImageDraw

back = Image.new('RGBA', (512,512), (255,255,255,0) )
backDraw = ImageDraw.Draw(back)
#backDraw.rectangle([ (,80), (200,200)], fill=(255,255,0,255))

print(back.size)
sub_size = (256,256)

for i in range(2):
    r1_pos = (132,259) #location in larger image
    r1 = Image.new('RGBA', sub_size )
    pdraw1 = ImageDraw.Draw(r1)
    pdraw1.line([ (0,0), r1.size], fill=(0,255,0,90), width = 15)

#r2_pos = (100,100) #location in larger image
#r2 = Image.new('RGBA', sub_size )
#pdraw2 = ImageDraw.Draw(r2)
#pdraw2.rectangle([ (0,0), (128,128)], fill=(0,255,0,90))

    back.paste(r1, r1_pos, mask=r1)
#back.paste(r2, r2_pos, mask=r2)
#back.save("a.png", "PNG")
back.show()

#                topLeftPt = (targetPos[0] * FACTOR - TAR_SIZE * FACTOR, targetPos[1] * FACTOR - TAR_SIZE * FACTOR)
#                bottomRightPt = (targetPos[0] * FACTOR + TAR_SIZE * FACTOR, targetPos[1] * FACTOR + TAR_SIZE * FACTOR)
#                obj_pos = (topLeftPt) #location in larger image
#                obj_win = Image.new('RGBA', (-topLeftPt[0] + bottomRightPt[0], -topLeftPt[1] + bottomRightPt[1]))
#                obj = ImageDraw.Draw(obj_win)
#                obj.ellipse([(0,0), obj_win.size], fill=(0,0,139,255)) # dark blue
#                self.window.paste(obj_win, obj_pos, mask=obj_win)


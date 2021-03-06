import bpy

#http://blenderartists.org/forum/showthread.php?239048-Store-Data-in-bpy


reordering = False
reorderingLabel = "Reorder"
directionIndex = -1
exists = False


#bpy.context.scene.text_blocks.clear()

def updateBookmarkList(self,context):

    bookmarkListDetect()    
    


class BookmarksLineNumbersPropertiesGroup(bpy.types.PropertyGroup):
    
    row_number = bpy.props.IntProperty()
    
 
bpy.utils.register_class(BookmarksLineNumbersPropertiesGroup)   
 
 
    
class detectionBookmarksPropertiesGroup(bpy.types.PropertyGroup):
    
    row_number = bpy.props.IntProperty()
    detection_string = bpy.props.StringProperty()
    indented = bpy.props.BoolProperty()
    name_short = bpy.props.StringProperty()    
    
    
bpy.utils.register_class(detectionBookmarksPropertiesGroup)



class textblocksPropertiesGroup(bpy.types.PropertyGroup):

    bookmarks_line_number = bpy.props.CollectionProperty(type=BookmarksLineNumbersPropertiesGroup)
    
    bookmarks_detection = bpy.props.CollectionProperty(type=detectionBookmarksPropertiesGroup)
   
   
bpy.utils.register_class(textblocksPropertiesGroup)



bpy.types.Scene.text_blocks = bpy.props.CollectionProperty(type=textblocksPropertiesGroup)

bpy.types.Scene.bookmark_name = bpy.props.StringProperty(description="Name of the new bookmark", default="Bookmark 1")

bpy.types.Scene.bookmark_type = bpy.props.EnumProperty(description = "The type of bookmark to manage", 
                                                       items = [("Line Number","Line Number","Line Number"),
                                                                ("Detection","Detection","Detection")]       
                                                       )
                                                                                                                                                                                                       
bpy.types.Scene.detect_classes = bpy.props.BoolProperty(default=True, update=updateBookmarkList)

bpy.types.Scene.detect_functions = bpy.props.BoolProperty(default=True, update=updateBookmarkList)

bpy.types.Scene.show_row_numbers = bpy.props.BoolProperty(default=False)

bpy.types.Scene.display_flat = bpy.props.BoolProperty(default=False)

bpy.types.Scene.display_prefix = bpy.props.BoolProperty(default=True)

bpy.types.Scene.bookmark_filter = bpy.props.StringProperty(options={"TEXTEDIT_UPDATE"})

bpy.context.scene.bookmark_name = "Bookmark"


bookmarkList = []#bpy.context.scene.text_blocks["Text Editor Bookmarks.py"].bookmarks



class BOOKMARK_LIST_OT_add(bpy.types.Operator):
    """Add a new bookmark on current line"""
    bl_idname = 'text.bookmark_list_add'
    bl_label = "Add new bookmark"

    def execute(self, context):

        bookmarkListAdd()

        return{'FINISHED'}



class BOOKMARK_LIST_OT_del(bpy.types.Operator):
    """Delete bookmark"""
    bl_idname      = 'text.bookmark_list_remove'
    bl_label       = "Remove bookmark"

    bookmarkName = bpy.props.StringProperty()

    def execute(self, context):
        
        bookmarkListRemove(self) 

        return{'FINISHED'}



class BOOKMARK_LIST_OT_select(bpy.types.Operator):
    """Go to bookmark"""
    bl_idname      = 'text.bookmark_list_select'
    bl_label       = "Select bookmark"
    
    bookmarkName = bpy.props.StringProperty()    
    
    def execute(self, context):
        
        bookmarkListSelect(self) 

        return{'FINISHED'}
   
    
    
class BOOKMARK_LIST_OT_reorder(bpy.types.Operator):
    """Reorder bookmarks"""
    bl_idname      = 'text.bookmark_list_reorder'
    bl_label       = "Reorder bookmarks"
     
    def execute(self, context):
        
        bookmarkListReorder() 

        return{'FINISHED'}  
    
    
    
class BOOKMARK_LIST_OT_move(bpy.types.Operator):
    """move bookmarks"""
    bl_idname      = 'text.bookmark_list_move'
    bl_label       = "Move bookmarks"
    
    direction = bpy.props.StringProperty()
    bookmarkName = bpy.props.StringProperty()
     
    def execute(self, context):
        
        bookmarkListMove(self) 

        return{'FINISHED'}        



class BOOKMARK_LIST_OT_detect(bpy.types.Operator):
    """Analyse the text block for bookmarks"""
    bl_idname = 'text.bookmark_list_detect'
    bl_label = "Detect Bookmarks"

    def execute(self, context):

        bookmarkListDetect()

        return{'FINISHED'}


def printList():
      
    print("")
    print("####Bookmarks##########")
    print("")      
        
    for textblock in bpy.context.scene.text_blocks:
        
        print("Textblock: "+textblock.name)
        print("")
        for bookmark in textblock.bookmarks_line_number:
            
            print("    Bookmark: "+bookmark.name)
            print("    Row number:"+str(bookmark.row_number))    
            print("")
printList()



def bookmarkListAdd():

    global bookmarkList
    
    textBlock = detectTextblock()        
    
    line_index = bpy.context.area.spaces.active.text.current_line_index
    
    newBookmark = textBlock.bookmarks_line_number.add()
    bookmarkList = textBlock.bookmarks_line_number
    
    inputBookmarkName = bpy.context.scene.bookmark_name
    
    if inputBookmarkName == "" or inputBookmarkName == "Bookmark":
        i = 1
        while "Bookmark "+str(i) in bookmarkList:
            i+=1
        newBookmark.name = "Bookmark "+str(i)
    else:
        if inputBookmarkName in bookmarkList:
            i = 1
            while inputBookmarkName+" "+str(i) in bookmarkList:
                i+=1
            newBookmark.name = inputBookmarkName+" "+str(i)
        else:                  
            newBookmark.name = inputBookmarkName
         
    newBookmark.row_number = line_index
        
    printList() 



def detectTextblock():
    global exists
    global bookmarkList
        
    for textBlock in bpy.context.scene.text_blocks:
        if bpy.context.area.spaces.active.text.name == textBlock.name:
            exists = True
            break
        else:
            exists = False
        

    if exists:
        #print("Text file does have bookmarks, use existing bookmark collection")
        textBlock = bpy.context.scene.text_blocks[bpy.context.area.spaces.active.text.name]
        
        if bpy.context.scene.bookmark_type == "Line Number":    
            
            bookmarkList = textBlock.bookmarks_line_number  
        
        elif bpy.context.scene.bookmark_type == "Detection":
            
            bookmarkList = textBlock.bookmarks_detection
        
    else:
        newTextBlock = bpy.context.scene.text_blocks.add()
        newTextBlock.name = bpy.context.area.spaces.active.text.name
        #print("Text file does not have bookmarks, adding")
        textBlock = bpy.context.scene.text_blocks[len(bpy.context.scene.text_blocks)-1]
        
    return textBlock
      
    
def bookmarkListRemove(self):
    
    for i, bookmark in enumerate(bookmarkList):
        print(bookmark)   
        if bookmark.name == self.bookmarkName:
            bookmarkList.remove(i)
    printList()
 
        
def bookmarkListSelect(self):

    for bookmark in bookmarkList:   
        if bookmark.name == self.bookmarkName:
            bpy.context.area.spaces.active.text.current_line_index = bookmark.row_number
                
    
    
def bookmarkListReorder():
    global reordering
    global reorderingLabel
    
    if reordering:
        reordering = False
        reorderingLabel = "Reorder"
    else:
        reordering = True    
        reorderingLabel = "Finish reordering"



def bookmarkListMove(self):

    for i, bookmark in enumerate(bookmarkList):   
        if bookmark.name == self.bookmarkName:
            if self.direction == "Up":
                bookmarkList.move(i,i-1)
            else:
                bookmarkList.move(i,i+1)
            print("current index "+str(i-1))
            print("target index  "+str(i+1))                

            break
    printList()
          
    
    
def bookmarkListDetect():
    
    textBlock = detectTextblock()
    
    print("Trying to detect bookmarks")
    print("") 
    
    textBlock.bookmarks_detection.clear()
        
    for index, line in enumerate(bpy.context.area.spaces.active.text.lines):
        
        lineWithoutSpaces = line.body.replace(" ","")
        
        if bpy.context.scene.detect_classes:
    
            if "class " in line.body and lineWithoutSpaces[0] == "c":
           
                newDetectedBookmark(textBlock, line, index, "class")
                                        
        if bpy.context.scene.detect_functions:
            
            if "def " in line.body and lineWithoutSpaces[0] == "d":
                
                newDetectedBookmark(textBlock, line, index, "def")
                


def newDetectedBookmark(textBlock, line, index, type):
    
    print(line.body)  

    newBookmark = textBlock.bookmarks_detection.add()
    newBookmark.name = line.body.split("(")[0]
    newBookmark.name_short = line.body.split(type,1)[1].split("(")[0]
    newBookmark.row_number = index
    newBookmark.detection_string = line.body
    
    if line.body[0] == " ":
        newBookmark.indented = True
    else:
        newBookmark.indented = False
        
    bookmarkList = textBlock.bookmarks_detection 
    
    

class BOOKMARK_LIST_PT(bpy.types.Panel):
    bl_label = "Bookmarks"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        global bookmarkList
        
        layout= self.layout
        
        row = layout.row()
        row.label(text="Bookmark type:")
        row = layout.row();
        row.prop(bpy.context.scene, "bookmark_type", expand=True)
        
        if bpy.context.scene.bookmark_type == "Line Number":
        
            row = layout.row()
            row.operator('text.bookmark_list_add', text="Add new bookmark", icon="ZOOMIN")
            row = layout.row()
            row.label(text="Bookmark Name:")
            row = layout.row()
            row.prop(bpy.context.scene, "bookmark_name",text="")
            row = layout.row()
            row.prop(bpy.context.area.spaces.active.text, "current_line_index", text="At Line")
            row = layout.row()
            row.label(text="Bookmark List:")

            if len(bookmarkList)<1:
                row = layout.row()
                row.enabled = False
                row.label(text="No bookmarks yet")
                
            if bpy.context.area.spaces.active.text.name in bpy.context.scene.text_blocks:        
                for bookmark in bpy.context.scene.text_blocks[bpy.context.area.spaces.active.text.name].bookmarks_line_number:   

                    bookmarkName = bookmark.name
                     
                    col = layout.column(align=True)
                    
                    if reordering:
                        row = col.row(align=True)
                        operatorProps = row.operator('text.bookmark_list_move',text = "", icon="TRIA_UP")
                        operatorProps.direction = "Up"
                        operatorProps.bookmarkName = bookmarkName 
                    
                    row = col.row(align=True)
                    row.operator('text.bookmark_list_select',text = bookmarkName).bookmarkName = bookmarkName            
                    row.operator('text.bookmark_list_remove',text ="", icon="X").bookmarkName = bookmarkName            
                    
                    if reordering:
                        row = col.row(align=True)
                        operatorProps = row.operator('text.bookmark_list_move',text = "", icon="TRIA_DOWN")
                        operatorProps.direction = "Down"
                        operatorProps.bookmarkName = bookmarkName  
                   
            row = layout.row(align=True)
            row.enabled = len(bookmarkList)>1
            row.operator('text.bookmark_list_reorder',text = reorderingLabel, icon="SEQ_SEQUENCER")                          
        
        elif bpy.context.scene.bookmark_type == "Detection":
                        
            row = layout.row()
            row.label(text="Detection")
            
            row = layout.row()
            row.operator("text.bookmark_list_detect", icon="VIEWZOOM")
            
            row = layout.row()
            row.label(text="Options:")
            
            row = layout.row()
            row.prop(bpy.context.scene, "bookmark_filter", text="Filter", icon="FILTER")
            
            row = layout.row()
            row.prop(bpy.context.scene, "detect_classes", text="Classes")
            row.prop(bpy.context.scene, "detect_functions", text="Functions")
            
            row = layout.row()
            row.prop(bpy.context.scene, "show_row_numbers", text="Row Numbers")
            row.prop(bpy.context.scene, "display_flat", text="Flat")
            
            row = layout.row()
            row.prop(bpy.context.scene, "display_prefix", text="Prefix")
            
            row = layout.row()
            row.label(text="Bookmarks:")
            
            if bpy.context.area.spaces.active.text.name in bpy.context.scene.text_blocks:        
                for bookmark in bpy.context.scene.text_blocks[bpy.context.area.spaces.active.text.name].bookmarks_detection:   
                    
                    if bpy.context.scene.bookmark_filter in bookmark.name or bpy.context.scene.bookmark_filter == "":
                                                                
                        if bpy.context.scene.display_prefix:
                                
                            bookmarkName = bookmark.name                                         
                            
                        else:
                        
                            bookmarkName = bookmark.name_short
                        
                        if bpy.context.scene.show_row_numbers:
                                                    
                            split = layout.split(percentage=0.15)
                            row = split.row()
                            row.label(text=str(bookmark.row_number))                      
                            
                            if bookmark.indented and not bpy.context.scene.display_flat:
                                row = split.row()
                                row.label(text="")
                            
                            row = split.row()
                            row.operator('text.bookmark_list_select',text = bookmarkName).bookmarkName = bookmarkName
                        
                        else:
                            
                            if bookmark.indented and not bpy.context.scene.display_flat:
                                split = layout.split(percentage=0.2)
                                row = split.row()
                                row.label(text="")
                                    
                                row = split.row()
                                row.operator('text.bookmark_list_select',text = bookmarkName).bookmarkName = bookmarkName      
                                
                            else:
                                
                                row = layout.row()
                                row.operator('text.bookmark_list_select',text = bookmarkName).bookmarkName = bookmarkName  
        
        row = layout.row()
        row.label(text="Rows: "+str(len(bpy.data.screens['Default.001'].areas[0].spaces[0].text.lines)))



classes = [BOOKMARK_LIST_PT, BOOKMARK_LIST_OT_add, BOOKMARK_LIST_OT_del, BOOKMARK_LIST_OT_select, BOOKMARK_LIST_OT_reorder, 
           BOOKMARK_LIST_OT_move, BOOKMARK_LIST_OT_detect]


def register():
    for className in classes:
        bpy.utils.register_class(className) 



def unregister():
    for className in classes:
        bpy.utils.unregister_class(className) 

#if __name__ == "__main__":
#    register()

register()

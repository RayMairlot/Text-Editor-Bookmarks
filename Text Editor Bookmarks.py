import bpy

#http://blenderartists.org/forum/showthread.php?239048-Store-Data-in-bpy


reordering = False
reorderingLabel = "Reorder"
directionIndex = -1
exists = False


#bpy.context.scene.text_blocks.clear()


class bookmarksPropertiesGroup(bpy.types.PropertyGroup):
    
    rowNumber = bpy.props.IntProperty()
    
 
bpy.utils.register_class(bookmarksPropertiesGroup)



class textblocksPropertiesGroup(bpy.types.PropertyGroup):

    bookmarks = bpy.props.CollectionProperty(type=bookmarksPropertiesGroup)
   
   
bpy.utils.register_class(textblocksPropertiesGroup)


bpy.types.Scene.text_blocks = bpy.props.CollectionProperty(type=textblocksPropertiesGroup)

bpy.types.Scene.bookmark_name = bpy.props.StringProperty(description="Name of the new bookmark", default="Bookmark 1")

bpy.types.Scene.bookmark_type = bpy.props.EnumProperty(description = "The type of bookmark to manage", 
                                                       items = [("Line Number","Line Number","Line Number"),
                                                              ("Detection","Detection","Detection")]       
                                                       )
                                                                                                      

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



def printList():
      
    print("")
    print("####Bookmarks##########")
    print("")      
        
    for textblock in bpy.context.scene.text_blocks:
        
        print("Textblock: "+textblock.name)
        print("")
        for bookmark in textblock.bookmarks:
            
            print("    Bookmark: "+bookmark.name)
            print("    Row number:"+str(bookmark.rowNumber))    
            print("")
printList()



def bookmarkListAdd():
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
        bookmarkList = textBlock.bookmarks    
        
    else:
        newTextBlock = bpy.context.scene.text_blocks.add()
        newTextBlock.name = bpy.context.area.spaces.active.text.name
        #print("Text file does not have bookmarks, adding")
        textBlock = bpy.context.scene.text_blocks[len(bpy.context.scene.text_blocks)-1]
        
    
    line_index = bpy.context.area.spaces.active.text.current_line_index
    
    newBookmark = textBlock.bookmarks.add()
    bookmarkList = textBlock.bookmarks
    
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
         
    newBookmark.rowNumber = line_index
    
    printList() 

    
    
def bookmarkListRemove(self):
    
    for i, bookmark in enumerate(bookmarkList):   
        if bookmark.name == self.bookmarkName:
            bookmarkList.remove(i)
    printList()
 
        
def bookmarkListSelect(self):
    
    for bookmark in bookmarkList:   
        if bookmark.name == self.bookmarkName:
            bpy.context.area.spaces.active.text.current_line_index = bookmark.rowNumber
                
    
    
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
                for bookmark in bpy.context.scene.text_blocks[bpy.context.area.spaces.active.text.name].bookmarks:   

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
        row.label(text="Rows: "+str(len(bpy.data.screens['Default.001'].areas[0].spaces[0].text.lines)))



classes = [BOOKMARK_LIST_PT, BOOKMARK_LIST_OT_add, BOOKMARK_LIST_OT_del, BOOKMARK_LIST_OT_select, BOOKMARK_LIST_OT_reorder, 
           BOOKMARK_LIST_OT_move]


def register():
    for className in classes:
        bpy.utils.register_class(className) 



def unregister():
    for className in classes:
        bpy.utils.unregister_class(className) 

#if __name__ == "__main__":
#    register()

register()

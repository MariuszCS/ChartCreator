import GUICreator
import PropertiesDictionaries

if (__name__ == "__main__"):
    while True:
        chart_creator = GUICreator.ChartCreator()
        main_frame = chart_creator.setup_main_frame()
        chart_creator.setup_menu(main_frame)
        chart_creator.setup_top_frame(main_frame)
        chart_creator.setup_right_frame(main_frame)
        chart_creator.setup_left_frame(main_frame)
        chart_creator.setup_bottom_frame(main_frame)
        chart_creator.run(main_frame)
        if (not chart_creator.new_file):
            break
        else:
            del chart_creator
            del main_frame
            
            

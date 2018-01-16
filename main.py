import GUICreator

if (__name__ == "__main__"):
    chart_creator = GUICreator.ChartCreator()
    main_frame = chart_creator.setup_main_frame()
    chart_creator.setup_menu(main_frame)
    chart_creator.setup_top_frame(main_frame)
    chart_creator.setup_right_frame(main_frame)
    chart_creator.setup_left_frame(main_frame)
    chart_creator.setup_bottom_frame(main_frame)
    chart_creator.run(main_frame)

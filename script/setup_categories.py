from model import Category
#goods
electronics = Category.new('electronics',Category.good())
	video_games = Category.new('video games',electronics)
		xbox = Category.new('xbox',video_games)
		ps3 = Category.new('ps3',video_games)
		wii = Category.new('wii',video_games)
	av = Category.new('av',electronics)
		tv = Category.new('tv',av)
		stereo = Category.new('stereo',av)

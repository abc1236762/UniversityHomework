cmake_minimum_required(VERSION 3.10)

set(HOMEWORK_ID 1010)

file(GLOB HOMEWORK_FILES ${HOMEWORK_ID}_*.c*)
foreach (HOMEWORK_FILE ${HOMEWORK_FILES})
	get_filename_component(FILE_EXT ${HOMEWORK_FILE} EXT)
	if (${FILE_EXT} STREQUAL ".c" OR (${FILE_EXT} STREQUAL ".i"))
		project(algorithm_homework C)
		set(CMAKE_C_STANDARD 99) # MAX=11 OJ=99
		add_executable(app ${HOMEWORK_FILE})
		break()
	elseif ((${FILE_EXT} STREQUAL ".cc") OR (${FILE_EXT} STREQUAL ".cp") OR
			(${FILE_EXT} STREQUAL ".cxx") OR (${FILE_EXT} STREQUAL ".cpp") OR
			(${FILE_EXT} STREQUAL ".CPP") OR (${FILE_EXT} STREQUAL ".c++") OR
			(${FILE_EXT} STREQUAL ".C") OR (${FILE_EXT} STREQUAL ".ii"))
		project(algorithm_homework CXX)
		set(CMAKE_CXX_STANDARD 11) # MAX=17 OJ=11
		add_executable(app ${HOMEWORK_FILE})
		break()
	endif ()
endforeach ()
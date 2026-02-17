include_guard(GLOBAL)

set(BUILD_TELEMETRY_DIR ${CMAKE_CURRENT_LIST_DIR})

function(configure_build_telemetry)
    if(NOT BUILD_TELEMETRY_CONFIGURATION)
        message(WARNING "Configuring Build Telemetry")

        # Check if the CMake version is at least 4.2
        if(CMAKE_VERSION VERSION_LESS "4.2")
            message(
                WARNING
                "CMake version is less than 4.2, configuring cmake_instrumentation is unavailable."
            )
            return()
        endif()

        if(CMAKE_MAJOR_VERSION EQUAL 4)
            if(CMAKE_MINOR_VERSION EQUAL 2)
                # Enable experimental feature for 4.2
                set(CMAKE_EXPERIMENTAL_INSTRUMENTATION
                    ec7aa2dc-b87f-45a3-8022-fe01c5f59984
                )
                #      elseif (CMAKE_MINOR_VERSION EQUAL 3)
                #        # Enable experimental feature for 4.3 -- ONCE WE HAVE THE GUID
                #        set(CMAKE_EXPERIMENTAL_INSTRUMENTATION ec7aa2dc-b87f-45a3-8022-fe01c5f59984)
            else()
                message(
                    WARNING
                    "Value for CMAKE_EXPERIMENTAL_INSTRUMENTATION is unknown, attempting to configure without gate set."
                )
            endif()
        endif()

        # Telemetry query
        cmake_instrumentation(
          API_VERSION 1
          DATA_VERSION 1

          OPTIONS staticSystemInformation dynamicSystemInformation trace
          HOOKS postGenerate preBuild postBuild preCMakeBuild postCMakeBuild postCMakeInstall postCTest
          CALLBACK ${BUILD_TELEMETRY_DIR}/telemetry.sh
        )
        message(
            WARNING
            "using callback script ${BUILD_TELEMETRY_DIR}/telemetry.sh"
        )

        # Mark configuration as done in cache
        set(BUILD_TELEMETRY_CONFIGURATION
            TRUE
            CACHE INTERNAL
            "Flag to ensure Bloomberg Build Telemetry configured only once"
        )
    endif()
endfunction(configure_build_telemetry)

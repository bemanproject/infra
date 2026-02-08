include_guard(GLOBAL)

cmake_minimum_required(VERSION 4.2)

set(BUILD_TELEMETRY_DIR ${CMAKE_CURRENT_LIST_DIR})

function(configure_build_telemetry)
  if(NOT BUILD_TELEMETRY_CONFIGURATION)
      message(WARNING "Configuring Bloomberg Build Telemetry")

    # Enable experimental feature!!
    set(CMAKE_EXPERIMENTAL_INSTRUMENTATION ec7aa2dc-b87f-45a3-8022-fe01c5f59984)

    # Telemetry query
    cmake_instrumentation(
      API_VERSION 1
      DATA_VERSION 1

      OPTIONS staticSystemInformation dynamicSystemInformation trace
      HOOKS postGenerate preBuild postBuild preCMakeBuild postCMakeBuild postCMakeInstall postCTest
      CALLBACK ${BUILD_TELEMETRY_DIR}/telemetry.sh
    )
    message(WARNING "using callback script ${BUILD_TELEMETRY_DIR}/telemetry.sh")

    # Mark task as done in cache
    set(BUILD_TELEMETRY_CONFIGURATION TRUE CACHE INTERNAL "Flag to ensure Bloomberg Build Telemetry configured only once")
  endif()

endfunction(configure_build_telemetry)

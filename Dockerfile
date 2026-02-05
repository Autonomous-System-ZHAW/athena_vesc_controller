FROM ros:humble

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=humble

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    python3-colcon-common-extensions \
    python3-rosdep \
    ros-humble-serial-driver \
    ros-humble-asio-cmake-module \
    ros-humble-ackermann-msgs \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Create workspace
WORKDIR /workspace

# Copy project files
COPY . /workspace/

# Update rosdep and install available dependencies
RUN rosdep update && \
    rosdep install --from-paths . -i -y --rosdistro $ROS_DISTRO || true

# Build the project
RUN bash -c 'source /opt/ros/$ROS_DISTRO/setup.bash && colcon build'

# Source setup in bashrc for interactive shells
RUN echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> /root/.bashrc && \
    echo "source /workspace/install/setup.bash" >> /root/.bashrc

# Set default command
CMD ["/bin/bash"]


